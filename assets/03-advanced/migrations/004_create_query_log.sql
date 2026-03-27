-- Migration 004: Create query_log table for search analytics
-- Tracks every search query through the MCP server for maintenance insights

CREATE TABLE IF NOT EXISTS query_log (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  query_text text NOT NULL,
  result_count integer,
  top_score float,
  search_mode text DEFAULT 'hybrid',
  vector_weight float,
  text_weight float,
  reranked boolean DEFAULT false,
  latency_ms integer,
  metadata jsonb DEFAULT '{}',
  created_at timestamptz DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_query_log_created_at ON query_log (created_at DESC);

-- RLS: restrict access to service role key only
ALTER TABLE query_log ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Service role full access" ON query_log
  FOR ALL USING (auth.role() = 'service_role');
