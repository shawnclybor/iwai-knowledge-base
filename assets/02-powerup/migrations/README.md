# Migrations

SQL migrations for setting up the Supabase database schema. Run these in order.

## Run Order

| # | File | What It Does |
|---|------|-------------|
| 1 | `001_create_file_metadata.sql` | Creates the `file_metadata` table for tracking ingested files (hash-based dedup, status tracking, extensible metadata) |
| 2 | `002_create_chunks.sql` | Creates the `chunks` table with pgvector embeddings (1536d) and auto-generated tsvector for full-text search. Adds HNSW, GIN, and file_id indexes. |
| 3 | `003_create_rpc_functions.sql` | Creates two RPC functions: `match_chunks` (pure vector similarity) and `hybrid_search` (vector + full-text with configurable weights) |

## How to Apply

### Option A: Supabase Dashboard (SQL Editor)

1. Open your Supabase project dashboard
2. Go to **SQL Editor**
3. Paste each migration file in order and run

### Option B: Claude with Supabase MCP

If Supabase MCP is connected, Claude can apply these directly:

```
Apply migration 001_create_file_metadata.sql to project bihjdegxbsdpekzclyxo
```

### Option C: Supabase CLI

```bash
supabase db push
```

## Notes

- Migration 002 enables the `vector` extension (pgvector). This is already available on all Supabase projects.
- The `file_metadata` table uses SHA256 hashes for dedup — if a file hasn't changed, it won't be re-processed.
- The `chunks` table auto-generates `content_tsv` from content using PostgreSQL's `to_tsvector('english', content)`.
