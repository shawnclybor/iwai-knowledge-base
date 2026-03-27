import { getSupabase } from "../lib/supabase.js";

export const listSourcesTool = {
  name: "list_sources",
  description:
    "List all files ingested into the knowledge base with their processing status and chunk counts.",
  inputSchema: {
    type: "object" as const,
    properties: {},
  },
};

export async function handleListSources(): Promise<string> {
  const supabase = getSupabase();

  const { data, error } = await supabase
    .from("file_metadata")
    .select("file_name, file_type, status, chunk_count, file_size, created_at")
    .order("file_name");

  if (error) {
    throw new Error(`Failed to query file_metadata: ${error.message}`);
  }

  if (!data || data.length === 0) {
    return "No files found in the knowledge base. Run Lesson 2's ingestion pipeline first.";
  }

  let output = "## Knowledge Base Sources\n\n";
  output += `**Total files:** ${data.length}\n\n`;
  output += "| File | Type | Status | Chunks | Size |\n";
  output += "|------|------|--------|--------|------|\n";

  let totalChunks = 0;

  for (const file of data) {
    const sizeKb = file.file_size
      ? `${(file.file_size / 1024).toFixed(1)} KB`
      : "—";
    output += `| ${file.file_name} | ${file.file_type} | ${file.status} | ${file.chunk_count ?? 0} | ${sizeKb} |\n`;
    totalChunks += file.chunk_count ?? 0;
  }

  output += `\n**Total chunks:** ${totalChunks}\n`;

  return output;
}
