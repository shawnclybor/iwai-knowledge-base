# Search and RPC — Technical Overview

Read this before running your first queries through the MCP server.

---

## What Happens When Claude Searches the KB

When you ask Claude a question like "What are the FMLA eligibility requirements?", the following happens behind the scenes:

```
You ask a question
    |
    v
Claude calls the search_kb MCP tool
    |
    v
MCP server receives the query text
    |
    v
1. EMBED: Query text -> OpenAI API -> 1536-dimension vector
    |
    v
2. SEARCH: Vector + query text -> Supabase RPC -> ranked results
    |
    v
3. (Optional) RERANK: Results -> GPT-4o-mini -> re-scored by relevance
    |
    v
4. LOG: Query, scores, latency -> query_log table
    |
    v
5. RETURN: Formatted results back to Claude
    |
    v
Claude reads the results and answers your question
```

Each step adds latency. A typical hybrid search takes ~90ms. Adding reranking adds ~1 second per 10 results. The query log records all of this so you can monitor performance.

## Key Terminology

### RPC (Remote Procedure Call)

An RPC is a function stored in the database that you call by name instead of writing raw SQL. Supabase lets you define these as PostgreSQL functions and call them over HTTP.

Lesson 2 created two RPCs:

- **`hybrid_search(query_embedding, query_text, ...)`** — Combines vector similarity with keyword matching. Takes both the embedding vector and the raw text so it can do both searches simultaneously, then merges the results with configurable weights.

- **`match_chunks(query_embedding, match_count)`** — Pure vector similarity search. Faster but misses exact keyword matches.

You don't write SQL to search the KB. You call these functions, and they handle the ranking and filtering internally.

### MCP (Model Context Protocol)

MCP is the protocol that lets Claude Code use external tools. An MCP server registers tools (like `search_kb`) that Claude can call during a conversation. The server runs locally via stdio — no ports, no networking, no deployment.

The `kb-search` MCP server wraps the Supabase RPCs into two tools:

| Tool | What it does |
|------|-------------|
| `search_kb` | Takes a question, embeds it, searches the KB, optionally reranks, logs the query, returns results |
| `list_sources` | Returns a table of all ingested files with their status and chunk counts |

### Hybrid Search

Hybrid search combines two search strategies:

- **Vector search** (semantic) — "What chunks have similar *meaning* to this query?" Uses the embedding vectors created in Lesson 2.
- **Full-text search** (keyword) — "What chunks contain these *exact words*?" Uses the tsvector index created in Lesson 2.

The results are merged with configurable weights (default: 70% vector, 30% keyword). This matters because:

- Pure vector search is great at semantic similarity but can miss exact terms like "FMLA" or "DOT"
- Pure keyword search finds exact terms but misses paraphrased or conceptual matches
- Hybrid search gives you both

### Reranking

Embedding similarity measures how close two texts are in meaning-space, but similarity is not the same as relevance. A chunk about "FMLA leave policies" and a chunk about "FMLA eligibility requirements" might have similar embeddings, but only one actually answers the question.

Reranking sends the top results to GPT-4o-mini with the original question and asks: "How relevant is this chunk to answering this question?" Each chunk gets a relevance score from 0-1, and the results are re-ordered.

**Tradeoff:** Better precision, but adds ~1 second of latency and costs a small amount per API call. Use it when precision matters more than speed.

### Query Logging

Every search through the MCP server is logged to the `query_log` table:

| Field | What it records |
|-------|----------------|
| `query_text` | The original question |
| `result_count` | How many chunks were returned |
| `top_score` | The highest similarity score |
| `search_mode` | "hybrid" or "vector" |
| `vector_weight` / `text_weight` | The weights used (hybrid only) |
| `reranked` | Whether reranking was applied |
| `latency_ms` | Total time for the search |

This data powers the maintenance workflow in Part 5. Zero-result queries reveal knowledge gaps. Low scores reveal retrieval problems. High latency reveals performance issues.

## The Two Search Modes

### Hybrid (default)

```
search_kb("What are the FMLA eligibility requirements?")
```

Calls `hybrid_search()` with default weights (0.7 vector, 0.3 text). Best for most queries — catches both semantic meaning and specific terms.

### Vector-only

```
search_kb("What are the FMLA eligibility requirements?", search_mode="vector")
```

Calls `match_chunks()` for pure embedding similarity. Faster (~60ms vs ~90ms) but can miss results that match on keywords but not semantics.

### Hybrid + Reranking

```
search_kb("What are the FMLA eligibility requirements?", rerank=true)
```

Same as hybrid, but the top results get re-scored by GPT-4o-mini. Slower (~1200ms) but more precise. Use when you need confidence in ranking.

## How This Connects to the Lessons

| Lesson | What it built | Role in search |
|--------|--------------|----------------|
| L1 (Core) | Structured KB files | The source content that gets searched |
| L2 (Power-Up) | Chunks, embeddings, RPCs, indexes | The searchable database and search functions |
| L3 (Advanced) | MCP server, query logging | The interface Claude uses to call the search functions |

The MCP server is a thin wrapper. The real search intelligence lives in the RPCs and indexes that Lesson 2 created. Lesson 3 makes them accessible and observable.
