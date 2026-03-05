-- 003: Create RPC functions for retrieval
-- Two search modes: pure vector similarity and hybrid (vector + full-text).

-- 1. Pure vector similarity search
CREATE OR REPLACE FUNCTION match_chunks(
  query_embedding vector(1536),
  match_threshold float DEFAULT 0.78,
  match_count int DEFAULT 10,
  filter_file_type text DEFAULT NULL
)
RETURNS TABLE (
  id uuid,
  file_id uuid,
  content text,
  similarity float,
  chunk_metadata jsonb,
  file_name text,
  file_type text
) AS $$
  SELECT
    c.id, c.file_id, c.content,
    1 - (c.embedding <=> query_embedding) AS similarity,
    c.chunk_metadata,
    f.file_name, f.file_type
  FROM chunks c
  JOIN file_metadata f ON f.id = c.file_id
  WHERE 1 - (c.embedding <=> query_embedding) > match_threshold
    AND (filter_file_type IS NULL OR f.file_type = filter_file_type)
  ORDER BY c.embedding <=> query_embedding
  LIMIT match_count;
$$ LANGUAGE sql STABLE;

-- 2. Hybrid search (vector + full-text)
CREATE OR REPLACE FUNCTION hybrid_search(
  query_text text,
  query_embedding vector(1536),
  match_count int DEFAULT 10,
  vector_weight float DEFAULT 0.7,
  text_weight float DEFAULT 0.3
)
RETURNS TABLE (
  id uuid,
  file_id uuid,
  content text,
  combined_score float,
  vector_score float,
  text_score float,
  file_name text
) AS $$
  WITH vector_results AS (
    SELECT c.id, c.file_id, c.content,
           1 - (c.embedding <=> query_embedding) AS score,
           f.file_name
    FROM chunks c
    JOIN file_metadata f ON f.id = c.file_id
    ORDER BY c.embedding <=> query_embedding
    LIMIT match_count * 3
  ),
  text_results AS (
    SELECT c.id, c.file_id, c.content,
           ts_rank(c.content_tsv, plainto_tsquery(query_text)) AS score,
           f.file_name
    FROM chunks c
    JOIN file_metadata f ON f.id = c.file_id
    WHERE c.content_tsv @@ plainto_tsquery(query_text)
    LIMIT match_count * 3
  )
  SELECT
    COALESCE(v.id, t.id) AS id,
    COALESCE(v.file_id, t.file_id) AS file_id,
    COALESCE(v.content, t.content) AS content,
    (COALESCE(v.score, 0) * vector_weight + COALESCE(t.score, 0) * text_weight) AS combined_score,
    COALESCE(v.score, 0) AS vector_score,
    COALESCE(t.score, 0) AS text_score,
    COALESCE(v.file_name, t.file_name) AS file_name
  FROM vector_results v
  FULL OUTER JOIN text_results t ON v.id = t.id
  ORDER BY combined_score DESC
  LIMIT match_count;
$$ LANGUAGE sql STABLE;
