-- 001: Create file_metadata table
-- Tracks every ingested file and its processing status.

CREATE TABLE IF NOT EXISTS file_metadata (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  file_name text NOT NULL,
  file_path text NOT NULL,
  file_type text NOT NULL,
  file_size bigint,
  file_hash text UNIQUE NOT NULL,
  chunk_count integer DEFAULT 0,
  chunk_strategy text,
  embedding_model text,
  status text NOT NULL DEFAULT 'processing',
  error_message text,
  metadata jsonb DEFAULT '{}',
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now(),
  processed_at timestamptz
);

-- Dedup check
CREATE UNIQUE INDEX IF NOT EXISTS idx_file_metadata_hash ON file_metadata (file_hash);

-- Auto-update updated_at on row change
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER file_metadata_updated_at
  BEFORE UPDATE ON file_metadata
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at();
