# Template: Upsert to Supabase

**Pipeline Stage:** 5 of 5
**Input:** Chunks with embeddings and metadata
**Output:** Populated `chunks` table, updated `file_metadata` status

---

## What This Step Does

Writes the embedded chunks to Supabase and updates the file tracking record. Uses transactions to keep data consistent — if anything fails, the file stays in `processing` status and can be retried.

## Process

### 1. Delete Old Chunks (if re-processing)

If the file already has chunks in the database (re-processing a changed file), delete them first:

```sql
DELETE FROM chunks WHERE file_id = '<file_metadata_id>';
```

### 2. Batch Insert Chunks

Insert chunks in batches of 100:

```sql
INSERT INTO chunks (file_id, chunk_index, content, embedding, token_count, chunk_metadata)
VALUES
  ('<file_id>', 0, 'chunk text...', '[0.123, -0.456, ...]', 142, '{"section_heading": "..."}'),
  ('<file_id>', 1, 'chunk text...', '[0.789, -0.012, ...]', 156, '{"section_heading": "..."}');
```

The `content_tsv` column auto-generates from `content` — don't set it manually.

### 3. Update File Metadata

After all chunks are inserted, update the tracking record:

```sql
UPDATE file_metadata
SET
  status = 'completed',
  chunk_count = <actual_count>,
  chunk_strategy = '<strategy_used>',
  embedding_model = 'text-embedding-3-small',
  processed_at = now()
WHERE id = '<file_metadata_id>';
```

### 4. Error Handling

If any step fails:

```sql
UPDATE file_metadata
SET
  status = 'failed',
  error_message = '<error details>'
WHERE id = '<file_metadata_id>';
```

Don't delete partially inserted chunks on failure — they'll be cleaned up on retry (Step 1 deletes old chunks before re-inserting).

## Verification

After this step, check:
- [ ] `file_metadata` shows all files with `status = 'completed'`
- [ ] `chunk_count` matches actual rows in `chunks` for each file
- [ ] No orphaned chunks (chunks without a valid file_id)
- [ ] `content_tsv` is populated (run a full-text search test)
- [ ] Embeddings are populated (run a similarity search test)

## Quick Sanity Queries

```sql
-- File processing summary
SELECT status, count(*) FROM file_metadata GROUP BY status;

-- Chunk counts per file
SELECT f.file_name, f.chunk_count, count(c.id) as actual_chunks
FROM file_metadata f
LEFT JOIN chunks c ON c.file_id = f.id
GROUP BY f.id, f.file_name, f.chunk_count;

-- Test full-text search
SELECT content FROM chunks
WHERE content_tsv @@ plainto_tsquery('safety policy')
LIMIT 3;

-- Test vector search (requires an embedding — use match_chunks RPC)
```
