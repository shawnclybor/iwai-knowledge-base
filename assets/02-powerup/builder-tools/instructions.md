# RAG Pipeline — Step-by-Step Instructions

This file walks through the complete RAG pipeline setup and execution. Follow each step in order.

> **Session management:** Long conversations use up context window. Start a new session at any `---` divider — your `.env` file and Supabase data persist between sessions. Good break points are marked with "Good place to start a new session" below.

---

## Prerequisites

Before starting, confirm you have:

- [ ] A Supabase project (free tier works) — you can create one directly via the Supabase MCP connector
- [ ] An OpenAI API key with access to `text-embedding-3-small`
- [ ] Claude Code or Cowork with the Supabase MCP connector enabled
- [ ] The source files from this lesson (in `source-files/`)

---

## Step 1: Environment Setup

### 1a: Supabase MCP Connector

The Supabase MCP connector handles database operations from Cowork — running migrations, executing queries, and verifying table state. Make sure it's connected in your Cowork MCP settings.

If you don't have a Supabase project yet, you can create one directly through the connector using the `create_project` tool — no need to leave Cowork.

### 1b: Environment Variables

The Python pipeline scripts connect to Supabase and OpenAI directly, so they need these environment variables **in addition to** the MCP connector:

```bash
export SUPABASE_URL="https://your-project.supabase.co"
export SUPABASE_KEY="your-service-role-key"
export OPENAI_API_KEY="sk-your-key"
```

> **Where to find the service role key:** Go to `https://supabase.com/dashboard/project/<YOUR_PROJECT_ID>/settings/api-keys`. Under **Secret keys**, copy the `default` secret key (click the eye icon to reveal it). Do **not** use the publishable key — that's the anon key for client-side use.

> **Why both?** The MCP connector lets Claude run SQL from the conversation. The env vars let the Python scripts (ingest, chunking, embedding) talk to Supabase and OpenAI on their own.

#### Claude setup instructions

Environment variables do NOT persist between bash calls in Cowork. Use this `.env` file approach:

1. Ask the student for their Supabase service role key and OpenAI API key.
2. Get the Supabase project URL from the MCP connector (`get_project` or `get_project_url`).
3. Write a `.env` file to `pipeline/scripts/.env` with all three variables:
   ```
   SUPABASE_URL=https://<project-id>.supabase.co
   SUPABASE_KEY=<service-role-key>
   OPENAI_API_KEY=<openai-key>
   ```
4. Add `python-dotenv` to `requirements.txt` and add `from dotenv import load_dotenv; load_dotenv()` to the top of each pipeline script so they auto-load the `.env` file.
5. As a fallback, source the `.env` file in the same bash call before running any script:
   ```bash
   set -a && source pipeline/scripts/.env && set +a && python <script>.py ...
   ```

### 1c: Python Dependencies

Install Python dependencies:

```bash
pip install -r pipeline/scripts/requirements.txt
```

**Or use the skill:** Run `/setup-rag` to walk through this automatically.

---

## Step 2: Create Database Schema

> Good place to start a new session if you completed Step 1 previously.

Apply the three migration files to your Supabase project. You can do this through the Supabase SQL Editor, the Supabase MCP, or the CLI.

### Migration 1: File Metadata Table

```sql
-- See migrations/001_create_file_metadata.sql
```

This creates the `file_metadata` table that tracks every file in the pipeline — its hash for dedup, processing status, and chunk count.

### Migration 2: Chunks Table

```sql
-- See migrations/002_create_chunks.sql
```

This creates the `chunks` table with:
- `vector(1536)` column for embeddings
- Auto-generated `tsvector` column for full-text search
- HNSW index for fast vector similarity search
- GIN index for fast full-text search

### Migration 3: Search Functions

```sql
-- See migrations/003_create_rpc_functions.sql
```

This creates two RPC functions:
- `match_chunks()` — Pure vector similarity search
- `hybrid_search()` — Combined vector + full-text search with configurable weights

**Verify:** After all migrations, run:
```sql
SELECT count(*) FROM file_metadata;
SELECT count(*) FROM chunks;
```
Both should return 0.

---

## Step 3: Review Source Files

Check what files are available for ingestion:

```bash
ls -la source-files/
```

You should see a mix of file types:
- `.md` — Markdown documents (handbooks, policies, memos)
- `.csv` — Tabular data (checklists, reference tables)
- `.docx` — Word documents (DOT drug testing policy, PTO policy)
- `.pdf` — PDF documents (DOL overtime rule, EEOC guidance)

Read the `source-files/README.md` for a complete inventory.

---

## Step 4: Run the Pipeline

> Good place to start a new session. Setup and schema are done — everything from here forward is pipeline execution.

The pipeline has five stages, all run as Python scripts.

### Stage 1: File Intake

```bash
cd pipeline/scripts
python ingest.py --source-dir ../../source-files --output-dir ./output
```

This scans all source files, computes SHA256 hashes for dedup, and registers them in `file_metadata`. Output is saved to `output/registered.json` — a manifest of files that need processing.

**Check:** Every file should show "New file" or "Skip (unchanged)." The manifest should list only files that need processing.

### Stage 2: Document Conversion

```bash
python convert.py --input ./output/registered.json --output-dir ./output
```

This converts each source file to normalized markdown using lightweight Python libraries (`python-docx` for Word, `pdfplumber` for PDF, stdlib for CSV/MD). It preserves heading hierarchy, table structure, and page boundaries. Output is saved to `output/converted.json`.

**Check:** Each file should convert successfully. Tables should be preserved as markdown. Heading hierarchy should be intact.

### Stage 3: Chunking

```bash
python chunking.py --input ./output/converted.json --output-dir ./output
```

This selects a chunking strategy per file type:
- Markdown/DOCX/PDF → Split at heading boundaries
- CSV → Group rows with column headers prepended

**Check:** Look at chunk counts and average token sizes. Target is ~600 tokens per chunk with some variation.

### Stage 4-5: Embedding + Upsert

```bash
python embed.py --input ./output/chunked.json
```

This sends each chunk to OpenAI for embedding, then writes everything to Supabase. Rate limit handling is built in.

**Check:** The summary at the end shows files processed, chunks inserted, and any failures.

**Or use the skill:** Run `/ingest` to execute all stages automatically with pre- and post-flight checks.

---

## Step 5: Verify Results

Run these queries to confirm everything worked:

```sql
-- Processing summary
SELECT status, count(*) FROM file_metadata GROUP BY status;

-- Chunks per file
SELECT f.file_name, f.chunk_count, f.chunk_strategy, f.file_type
FROM file_metadata f
WHERE f.status = 'completed'
ORDER BY f.file_name;

-- Total chunks and token stats
SELECT
  count(*) as total_chunks,
  avg(token_count)::int as avg_tokens,
  min(token_count) as min_tokens,
  max(token_count) as max_tokens
FROM chunks;

-- Test full-text search
SELECT left(content, 100), file_id
FROM chunks
WHERE content_tsv @@ plainto_tsquery('workers compensation')
LIMIT 3;
```

---

## Step 6: Test Retrieval

> Good place to start a new session. Data is in Supabase — calibration and review are independent of the ingestion context.

Use the calibrate skill to run test queries:

```
/calibrate
```

Or run individual queries:

```
/calibrate "What are the FMLA eligibility requirements?"
```

This generates an embedding for your query, runs hybrid search, and shows the top results with relevance scores.

### Sample Queries to Try

1. "What are the workers compensation requirements in North Carolina?"
2. "How should we classify subcontractors vs employees?"
3. "What is the DOT drug testing policy for CDL drivers?"
4. "What are the new overtime salary thresholds for 2024?"
5. "FMLA eligibility requirements"

---

## Step 7: Quality Review (Optional)

Launch the review agent for a comprehensive quality audit:

The `rag-reviewer` agent checks:
- Database health (file statuses, orphaned chunks, null embeddings)
- Chunk quality (token distribution, too-small/too-large chunks)
- Metadata completeness
- Search readiness (indexes, full-text search)

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `SUPABASE_URL not set` | Set environment variables (Step 1) |
| `relation "file_metadata" does not exist` | Run migrations (Step 2) |
| `openai.RateLimitError` | The script auto-retries with backoff. If persistent, wait 60 seconds and re-run. |
| `0 files to process` | Files already ingested. Delete from `file_metadata` to re-process, or modify source files. |
| Chunks too small/large | Adjust `MAX_CHUNK_TOKENS` in `chunking.py` (default: 600) |
| Poor search results | Try adjusting hybrid search weights in `/calibrate`. More semantic weight (0.8/0.2) helps for conceptual queries; more full-text weight (0.3/0.7) helps for keyword-specific queries. |
