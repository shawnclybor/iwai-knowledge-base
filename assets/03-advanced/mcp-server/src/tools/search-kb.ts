import { z } from "zod";
import { getSupabase, getOpenAI, embedQuery } from "../lib/supabase.js";

interface SearchResult {
  id: string;
  file_id: string;
  content: string;
  score: number;
  vector_score?: number;
  text_score?: number;
  file_name: string;
  rerank_score?: number;
}

export const searchKbSchema = {
  query: z.string().describe("Natural language search query"),
  search_mode: z.enum(["hybrid", "vector"]).default("hybrid").describe(
    "Search mode: 'hybrid' uses vector + full-text search (default), 'vector' uses pure vector similarity"
  ),
  match_count: z.number().default(10).describe("Maximum number of results to return (default: 10)"),
  vector_weight: z.number().default(0.7).describe("Weight for vector similarity in hybrid mode, 0-1 (default: 0.7)"),
  text_weight: z.number().default(0.3).describe("Weight for keyword matching in hybrid mode, 0-1 (default: 0.3)"),
  rerank: z.boolean().default(false).describe("Re-rank results using GPT-4o-mini for improved precision (default: false)"),
};

export const SEARCH_KB_DESCRIPTION =
  "Search the knowledge base using semantic and/or keyword search. " +
  "Supports hybrid mode (vector + full-text), vector-only mode, and optional LLM-based reranking.";

type SearchKbArgs = {
  query: string;
  search_mode?: "hybrid" | "vector";
  match_count?: number;
  vector_weight?: number;
  text_weight?: number;
  rerank?: boolean;
};

export async function handleSearchKb(args: SearchKbArgs): Promise<string> {
  const {
    query,
    search_mode = "hybrid",
    match_count = 10,
    vector_weight = 0.7,
    text_weight = 0.3,
    rerank = false,
  } = args;

  // Validate inputs
  if (!query || query.trim().length === 0) {
    throw new Error("Query cannot be empty.");
  }

  const startTime = Date.now();
  const supabase = getSupabase();

  // Step 1: Embed the query
  const queryEmbedding = await embedQuery(query);

  // Step 2: Search based on mode
  let results: SearchResult[];

  if (search_mode === "vector") {
    const { data, error } = await supabase.rpc("match_chunks", {
      query_embedding: queryEmbedding,
      match_threshold: 0.78,
      match_count: rerank ? match_count * 2 : match_count,
    });

    if (error) {
      throw new Error(`Vector search failed: ${error.message}`);
    }

    results = (data || []).map((row: any) => ({
      id: row.id,
      file_id: row.file_id,
      content: row.content,
      score: row.similarity,
      file_name: row.file_name,
    }));
  } else {
    const { data, error } = await supabase.rpc("hybrid_search", {
      query_text: query,
      query_embedding: queryEmbedding,
      match_count: rerank ? match_count * 2 : match_count,
      vector_weight,
      text_weight,
    });

    if (error) {
      throw new Error(`Hybrid search failed: ${error.message}`);
    }

    results = (data || []).map((row: any) => ({
      id: row.id,
      file_id: row.file_id,
      content: row.content,
      score: row.combined_score,
      vector_score: row.vector_score,
      text_score: row.text_score,
      file_name: row.file_name,
    }));
  }

  // Step 3: Optional reranking
  if (rerank && results.length > 0) {
    try {
      results = await rerankResults(query, results);
      results = results.slice(0, match_count);
    } catch {
      // Reranking failed — fall back to original order
      results = results.slice(0, match_count);
    }
  }

  const latencyMs = Date.now() - startTime;

  // Step 4: Log to query_log (fire and forget)
  logQuery(supabase, {
    query_text: query,
    result_count: results.length,
    top_score: results[0]?.score ?? 0,
    search_mode,
    vector_weight: search_mode === "hybrid" ? vector_weight : null,
    text_weight: search_mode === "hybrid" ? text_weight : null,
    reranked: rerank,
    latency_ms: latencyMs,
  }).catch(() => {
    // Non-blocking — don't fail the search if logging fails
  });

  // Step 5: Format output
  if (results.length === 0) {
    return `No results found for: "${query}"\n\nTry broadening your query or switching search modes.`;
  }

  let output = `## Search Results for: "${query}"\n`;
  output += `**Mode:** ${search_mode}${rerank ? " + reranking" : ""} | **Results:** ${results.length} | **Latency:** ${latencyMs}ms\n\n`;

  for (let i = 0; i < results.length; i++) {
    const r = results[i];
    output += `### ${i + 1}. ${r.file_name}\n`;
    output += `**Score:** ${r.score.toFixed(4)}`;
    if (r.vector_score !== undefined) {
      output += ` (vector: ${r.vector_score.toFixed(4)}, text: ${(r.text_score ?? 0).toFixed(4)})`;
    }
    if (r.rerank_score !== undefined) {
      output += ` | **Rerank:** ${r.rerank_score.toFixed(2)}`;
    }
    output += "\n\n";
    output += r.content.slice(0, 500);
    if (r.content.length > 500) output += "...";
    output += "\n\n---\n\n";
  }

  return output;
}

/**
 * Re-rank results using GPT-4o-mini to score relevance.
 */
async function rerankResults(
  query: string,
  results: SearchResult[]
): Promise<SearchResult[]> {
  const openai = getOpenAI();

  const scored = await Promise.all(
    results.map(async (result) => {
      const response = await openai.chat.completions.create({
        model: "gpt-4o-mini",
        messages: [
          {
            role: "system",
            content:
              "Rate the relevance of the following text passage to the query. " +
              "Return ONLY a number between 0 and 1, where 1 is perfectly relevant. " +
              "No explanation.",
          },
          {
            role: "user",
            content: `Query: ${query}\n\nPassage: ${result.content.slice(0, 1000)}`,
          },
        ],
        temperature: 0,
        max_tokens: 5,
      });

      const scoreText = response.choices[0]?.message?.content?.trim() ?? "0";
      const rerankScore = parseFloat(scoreText) || 0;

      return { ...result, rerank_score: rerankScore };
    })
  );

  return scored.sort((a, b) => (b.rerank_score ?? 0) - (a.rerank_score ?? 0));
}

/**
 * Log a search query to the query_log table (async, non-blocking).
 */
async function logQuery(
  supabase: any,
  entry: {
    query_text: string;
    result_count: number;
    top_score: number;
    search_mode: string;
    vector_weight: number | null;
    text_weight: number | null;
    reranked: boolean;
    latency_ms: number;
  }
): Promise<void> {
  await supabase.from("query_log").insert(entry);
}
