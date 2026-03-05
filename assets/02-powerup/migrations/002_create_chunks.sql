-- 002: Create chunks table with vector + full-text search indexes
-- Stores content chunks with embeddings for similarity and hybrid search.

-- Enable pgvector if not already enabled
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS chunks (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  file_id uuid NOT NULL REFERENCES file_metadata(id) ON DELETE CASCADE,
  chunk_index integer NOT NULL,
  content text NOT NULL,
  content_tsv tsvector GENERATED ALWAYS AS (to_tsvector('english', content)) STORED,
  embedding vector(1536),
  token_count integer,
  chunk_metadata jsonb DEFAULT '{}',
  created_at timestamptz DEFAULT now()
);

-- Vector similarity search (HNSW for fast approximate nearest neighbor)
CREATE INDEX IF NOT EXISTS idx_chunks_embedding ON chunks
  USING hnsw (embedding vector_cosine_ops);

-- Full-text search
CREATE INDEX IF NOT EXISTS idx_chunks_content_tsv ON chunks
  USING gin (content_tsv);

-- File lookup
CREATE INDEX IF NOT EXISTS idx_chunks_file_id ON chunks (file_id);
