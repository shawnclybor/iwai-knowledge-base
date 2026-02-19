# IWAI RAG Knowledge Base Pipeline — Implementation Plan

**Date:** February 11, 2026
**Project:** iwai-knowledge-base
**Supabase Project:** IWAI Lessons (`bihjdegxbsdpekzclyxo`)
**Status:** Plan — awaiting approval

---

## 1. Goals

Build a reusable RAG ingestion pipeline that:

1. Accepts **docx, pdf, md, and csv** files from a source folder
2. Uses **Docling MCP** to convert documents into a normalized format (markdown)
3. Applies **dynamic chunking** — selecting the best strategy per document type
4. Upserts results into **Supabase** across two tables: `file_metadata` and `chunks`
5. Provides a **retrieval calibration** layer for tuning search quality

**Key improvement over KnoPro chatbot approach:** structured 2-table schema, Docling-based conversion (vs manual prep), dynamic chunking (vs one-size-fits-all), hash-based change detection, and built-in calibration harness.

---

## 2. Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     SOURCE FILES                            │
│            docx  │  pdf  │  md  │  csv                      │
└────────┬────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────┐
│   FILE INTAKE       │
│  • Hash (SHA256)    │
│  • Dedup check      │
│  • Insert metadata  │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│   DOCLING MCP       │
│  • Convert to MD    │
│  • Extract structure│
│  • Preserve tables  │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│   CHUNKING ROUTER   │
│  • Analyze structure│
│  • Select strategy  │
│  • Generate chunks  │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│   EMBEDDING         │
│  • Batch embed      │
│  • Model: TBD       │
└────────┬────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│           SUPABASE (pgvector)           │
│  ┌──────────────┐  ┌────────────────┐   │
│  │ file_metadata │  │    chunks      │   │
│  │ (tracking)    │←─│ (embeddings)   │   │
│  └──────────────┘  └────────────────┘   │
│           ↕                              │
│  ┌──────────────────────────────┐       │
│  │  RETRIEVAL CALIBRATION       │       │
│  │  • Similarity search (RPC)   │       │
│  │  • Hybrid search (vector+FTS)│       │
│  │  • Configurable thresholds   │       │
│  └──────────────────────────────┘       │
└─────────────────────────────────────────┘
```

---

## 3. Database Schema

### Table: `file_metadata`

Tracks every ingested file and its processing status.

| Column | Type | Notes |
|--------|------|-------|
| `id` | uuid (PK) | `gen_random_uuid()` |
| `file_name` | text | Original filename |
| `file_path` | text | Source path |
| `file_type` | text | `docx`, `pdf`, `md`, `csv` |
| `file_size` | bigint | Bytes |
| `file_hash` | text (unique) | SHA256 — dedup + change detection |
| `chunk_count` | integer | Number of chunks generated |
| `chunk_strategy` | text | Which strategy was applied |
| `embedding_model` | text | Model used (e.g. `text-embedding-3-small`) |
| `status` | text | `processing`, `completed`, `failed`, `stale` |
| `error_message` | text | Nullable — failure details |
| `metadata` | jsonb | Extensible: page_count, word_count, author, title, etc. |
| `created_at` | timestamptz | Default `now()` |
| `updated_at` | timestamptz | Auto-updated |
| `processed_at` | timestamptz | When ingestion completed |

### Table: `chunks`

Stores the actual content chunks with their embeddings.

| Column | Type | Notes |
|--------|------|-------|
| `id` | uuid (PK) | `gen_random_uuid()` |
| `file_id` | uuid (FK) | References `file_metadata.id`, `ON DELETE CASCADE` |
| `chunk_index` | integer | Order within document |
| `content` | text | Chunk text |
| `content_tsv` | tsvector | Generated from `content` — for full-text search |
| `embedding` | vector(1536) | Vector embedding (dimension depends on model) |
| `token_count` | integer | Useful for retrieval calibration |
| `chunk_metadata` | jsonb | Section heading, page number, hierarchy level, etc. |
| `created_at` | timestamptz | Default `now()` |

### Indexes

```sql
-- Vector similarity search (HNSW for fast ANN)
CREATE INDEX idx_chunks_embedding ON chunks
  USING hnsw (embedding vector_cosine_ops);

-- Full-text search
CREATE INDEX idx_chunks_content_tsv ON chunks
  USING gin (content_tsv);

-- File lookup
CREATE INDEX idx_chunks_file_id ON chunks (file_id);

-- Dedup check
CREATE UNIQUE INDEX idx_file_metadata_hash ON file_metadata (file_hash);
```

### RPC Functions (Supabase)

```sql
-- 1. Similarity search
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
```

---

## 4. Pipeline Steps (Detail)

### Step 1: File Intake

- Scan source folder for supported file types (`.docx`, `.pdf`, `.md`, `.csv`)
- Compute SHA256 hash for each file
- Check `file_metadata` for existing hash:
  - **Hash exists + status=completed** → Skip (file unchanged)
  - **Hash exists + status=failed** → Retry
  - **Hash not found** → New file, insert row with `status='processing'`
- Record file_name, file_path, file_type, file_size

### Step 2: Docling Conversion

- Call `convert_document_into_docling_document(source=file_path)` for each file
- Export to markdown via `export_docling_document_to_markdown(document_key)`
- For **CSV files**: two options —
  - Option A: Docling converts to markdown table
  - Option B: Custom handler — read with pandas, format rows as natural language
- Store the Docling `document_key` for downstream operations
- Extract structural info via `get_overview_of_document_anchors(document_key)` to inform chunking

### Step 3: Chunking Router

Analyzes the converted document and selects the best chunking strategy:

| File Type | Primary Strategy | Fallback | Notes |
|-----------|-----------------|----------|-------|
| **PDF** | Document-structure (headings/sections from Docling) | Recursive with overlap | Docling preserves heading hierarchy, tables |
| **DOCX** | Document-structure (heading levels) | Recursive with overlap | Word docs typically have clear H1/H2/H3 |
| **MD** | Header-based splitting (## and ###) | Recursive with overlap | Already structured |
| **CSV** | Row-group chunking | Per-row with header prepend | Each chunk = N rows with column context |

**Common parameters:**
- Max chunk size: ~600 tokens (tunable)
- Overlap: 10-15% between adjacent chunks
- Minimum chunk size: 50 tokens (merge small fragments with neighbors)

**Chunk metadata** captured per chunk:
- `section_heading` — nearest heading above the chunk
- `chunk_index` — position in document
- `page_number` — if available from Docling
- `hierarchy_level` — heading depth (1, 2, 3...)
- `has_table` — boolean, if chunk contains tabular data

### Step 4: Embedding

- Batch embed all chunks for a given file
- Model choice (to be confirmed):
  - **OpenAI `text-embedding-3-small`** — 1536 dims, $0.02/1M tokens, good baseline
  - **OpenAI `text-embedding-3-large`** — 3072 dims, better quality, 2x cost
  - **Open-source alternative** — e.g., `bge-large-en-v1.5` for zero API cost
- Batch size: 100 chunks per API call (OpenAI max is 2048)

### Step 5: Upsert to Supabase

- Within a transaction:
  1. Delete existing chunks for this file_id (if re-processing)
  2. Batch insert new chunks (100 per batch)
  3. Update `file_metadata`: status, chunk_count, chunk_strategy, embedding_model, processed_at
- Error handling: set `status='failed'` and `error_message` on any failure

---

## 5. Retrieval Calibration

The "tuning knobs" available after ingestion is complete:

### 5a. Configurable Parameters

| Parameter | Default | Range | Purpose |
|-----------|---------|-------|---------|
| `match_threshold` | 0.78 | 0.5–0.95 | Minimum similarity to return |
| `match_count` | 10 | 1–50 | Top-K results |
| `vector_weight` | 0.7 | 0–1 | Weight for semantic similarity in hybrid |
| `text_weight` | 0.3 | 0–1 | Weight for keyword match in hybrid |
| `rerank_enabled` | false | bool | Whether to apply re-ranking |
| `mmr_lambda` | 0.5 | 0–1 | Diversity vs relevance tradeoff |

### 5b. Search Modes

1. **Pure vector search** — best for exploratory/semantic queries
2. **Hybrid search** (vector + full-text) — best for queries with specific terms/jargon
3. **Filtered search** — vector search constrained by metadata (file_type, date, etc.)

### 5c. Evaluation Framework

- Create a test set of ~20-30 representative queries
- For each query, manually label the "expected" relevant chunks
- Metrics: Precision@K, Recall@K, MRR (Mean Reciprocal Rank)
- Compare across search modes and parameter settings
- Iterate: adjust thresholds, try re-ranking, adjust chunk sizes

---

## 6. Implementation Phases

### Phase 1: Database Foundation
- [ ] Create `file_metadata` table with indexes
- [ ] Create `chunks` table with vector + FTS indexes
- [ ] Create `match_chunks` and `hybrid_search` RPC functions
- [ ] Decide: migrate existing 184 rows or start fresh

### Phase 2: Ingestion Pipeline (Python)
- [ ] File intake module (hash, dedup, metadata insert)
- [ ] Docling MCP integration (convert + export to markdown)
- [ ] ChunkingRouter with per-type strategies
- [ ] Embedding module (batch API calls)
- [ ] Supabase upsert module (transactional batch insert)
- [ ] End-to-end test with one file of each type

### Phase 3: Retrieval Calibration
- [ ] Build search test harness
- [ ] Create evaluation query set
- [ ] Implement hybrid search tuning
- [ ] Test and compare search modes
- [ ] Document optimal settings

### Phase 4: Operations & Maintenance
- [ ] Change detection (re-process on hash change)
- [ ] Stale content flagging
- [ ] Batch re-embedding support (model upgrades)
- [ ] Logging and error reporting

---

## 7. Open Questions

These decisions should be made before implementation begins:

1. **Embedding model** — OpenAI `text-embedding-3-small` (1536d, cheap) vs `text-embedding-3-large` (3072d, better) vs open-source?
2. **Existing data** — Migrate the 184 rows in "IWAI Test Database" to the new schema, or start fresh?
3. **Runtime** — Local Python script, Supabase Edge Function, or both?
4. **CSV handling** — Row-per-chunk vs natural-language-summary chunks?
5. **Re-ranking** — Add a cross-encoder re-ranker (e.g., Cohere rerank) or keep it simple initially?
6. **Source folder** — Where will source documents live? Local filesystem, Google Drive, or Supabase Storage?

---

## 8. Tech Stack Summary

| Component | Tool | Notes |
|-----------|------|-------|
| Document conversion | Docling MCP | Handles all 4 file types → markdown |
| Chunking | Python (custom) | ChunkingRouter with per-type strategies |
| Embedding | OpenAI API (TBD) | Batch embedding |
| Vector store | Supabase pgvector | Already enabled on IWAI Lessons project |
| Full-text search | PostgreSQL tsvector | Built into Supabase |
| Pipeline orchestration | Python script | Could wrap in Edge Function later |
| Retrieval | Supabase RPC functions | match_chunks, hybrid_search |
