import { createClient, SupabaseClient } from "@supabase/supabase-js";
import OpenAI from "openai";

const EMBEDDING_MODEL = "text-embedding-3-small";
const EMBEDDING_DIMENSIONS = 1536;

let supabaseClient: SupabaseClient | null = null;
let openaiClient: OpenAI | null = null;

export function getSupabase(): SupabaseClient {
  if (supabaseClient) return supabaseClient;

  const url = process.env.SUPABASE_URL;
  const key = process.env.SUPABASE_KEY;

  if (!url || !key) {
    throw new Error(
      "Missing SUPABASE_URL or SUPABASE_KEY environment variables. " +
        "Set them in .mcp.json env or export them in your shell."
    );
  }

  supabaseClient = createClient(url, key);
  return supabaseClient;
}

export function getOpenAI(): OpenAI {
  if (openaiClient) return openaiClient;

  const apiKey = process.env.OPENAI_API_KEY;

  if (!apiKey) {
    throw new Error(
      "Missing OPENAI_API_KEY environment variable. " +
        "Set it in .mcp.json env or export it in your shell."
    );
  }

  openaiClient = new OpenAI({ apiKey });
  return openaiClient;
}

/**
 * Embed a text query using OpenAI text-embedding-3-small (1536 dimensions).
 */
export async function embedQuery(text: string): Promise<number[]> {
  const openai = getOpenAI();

  const response = await openai.embeddings.create({
    model: EMBEDDING_MODEL,
    input: text,
  });

  return response.data[0].embedding;
}

/**
 * Validate that all required environment variables are set.
 * Call this at server startup to fail fast with clear errors.
 */
export function validateEnv(): void {
  const required = ["SUPABASE_URL", "SUPABASE_KEY", "OPENAI_API_KEY"];
  const missing = required.filter((key) => !process.env[key]);

  if (missing.length > 0) {
    throw new Error(
      `Missing required environment variables: ${missing.join(", ")}. ` +
        "Check your .mcp.json env configuration."
    );
  }
}
