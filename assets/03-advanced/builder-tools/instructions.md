# Lesson 3: Advanced — Step-by-Step Workflow

Follow these 7 steps in order. Each step builds on the previous one.

---

## Step 1: Check Prerequisites

Before anything else, verify:

1. **Node.js >= 18** — run `node --version`. If missing or outdated, install from [nodejs.org](https://nodejs.org/).
2. **Python 3.10+** — run `python --version`. Should already be installed from Lesson 2.
3. **Lesson 2 completed** — the Supabase database must have embedded chunks from L2's pipeline. Verify with:

```sql
-- Should return rows with status = 'completed'
SELECT status, count(*) FROM file_metadata GROUP BY status;

-- Should return a number > 0
SELECT count(*) FROM chunks WHERE embedding IS NOT NULL;

-- Both RPC functions must exist
SELECT proname FROM pg_proc WHERE proname IN ('hybrid_search', 'match_chunks');
```

If any check fails, go back and complete Lesson 2 first.

---

## Step 2: Environment Setup

Set up environment variables and install dependencies.

**Environment variables** — write to `assets/03-advanced/.env`:

```bash
# Reuse from Lesson 2
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-service-role-key
OPENAI_API_KEY=sk-your-openai-key

# New for Lesson 3 — sign up at https://langfuse.com
# Go to Settings → API Keys to get these values
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_HOST=https://cloud.langfuse.com

# Resume flags (set automatically by commands)
SETUP_COMPLETE=0
MCP_SERVER_READY=0
EVALUATION_COMPLETE=0
```

**Tip:** If you completed Lesson 2, check `assets/02-powerup/pipeline/scripts/.env` for your Supabase and OpenAI keys.

**Install dependencies:**

```bash
# MCP server (TypeScript)
cd assets/03-advanced/mcp-server && npm install

# Evaluation harness (Python)
pip install -r assets/03-advanced/evaluation/requirements.txt
```

---

## Step 3: Apply Migration

Apply the new `query_log` table migration to your Supabase project:

```sql
-- Run via Supabase MCP or dashboard
-- File: assets/03-advanced/migrations/004_create_query_log.sql
```

Verify the table exists:

```sql
SELECT count(*) FROM query_log;  -- Should return 0
```

---

## Step 4: Build + Deploy MCP Server

**Read first:** `templates/mcp-server-build.md`

This step configures the custom MCP server that gives Claude direct access to the knowledge base.

**What the MCP server does:**
- `search_kb` — embeds your query via OpenAI, searches Supabase via `hybrid_search()` or `match_chunks()`, optionally re-ranks results with GPT-4o-mini
- `list_sources` — lists all ingested files from `file_metadata`

**Configure `.mcp.json` at the repo root:**

The setup command merges this into your existing `.mcp.json` (if any):

```json
{
  "mcpServers": {
    "kb-search": {
      "command": "npx",
      "args": ["tsx", "src/index.ts"],
      "cwd": "assets/03-advanced/mcp-server",
      "env": {
        "SUPABASE_URL": "your-url",
        "SUPABASE_KEY": "your-key",
        "OPENAI_API_KEY": "your-key"
      }
    }
  }
}
```

**Restart Claude Code** to load the new MCP server. Then verify:

```
> Ask Claude: "What tools do you have from the kb-search server?"
> Expected: search_kb and list_sources
```

---

## Step 5: Test Search + Reranking

Run these 5 queries through the MCP server, comparing modes:

| # | Query |
|---|-------|
| 1 | "What are the FMLA eligibility requirements?" |
| 2 | "Workers compensation requirements in North Carolina" |
| 3 | "How should we classify subcontractors vs employees?" |
| 4 | "DOT drug testing policy for CDL drivers" |
| 5 | "New overtime salary thresholds 2024" |

**Compare:**
1. **Hybrid mode** (default) — `search_mode: "hybrid"`
2. **Vector-only mode** — `search_mode: "vector"`
3. **Hybrid + reranking** — `rerank: true`

Observe how results change across modes. Hybrid mode typically outperforms vector-only for queries with specific terms (like "DOT" or "FMLA"). Reranking improves precision by using GPT-4o-mini to judge relevance.

---

## Step 6: Run Evaluation

**Read first:** `templates/evaluation-harness.md`

Run the evaluation harness to score retrieval quality:

```bash
cd assets/03-advanced/evaluation
python evaluate.py
```

This runs 15-20 test queries against the knowledge base, generates answers, and scores them with Ragas metrics:

- **Context Precision** — are relevant chunks ranked higher?
- **Faithfulness** — is the answer grounded in the retrieved context?
- **Answer Relevancy** — does the answer actually address the question?

Results are pushed to your Langfuse dashboard (URL printed by the script). Open it to explore traces — each trace shows the embedding, retrieval, and generation spans with scores attached.

---

## Step 7: Maintenance Workflow

**Read first:** `templates/maintenance-ops.md`

Now that the knowledge base is live, establish a maintenance routine.

**Query log analysis** — check what's being searched:

```sql
-- Total queries and average latency
SELECT count(*), avg(latency_ms) FROM query_log;

-- Queries with zero results (gaps in knowledge)
SELECT query_text, created_at FROM query_log WHERE result_count = 0 ORDER BY created_at DESC;

-- Most common search modes
SELECT search_mode, reranked, count(*) FROM query_log GROUP BY search_mode, reranked;
```

**Stale content detection** — check if source files have changed since last ingestion:

Compare current file hashes against `file_metadata.file_hash`. If any file has changed, re-ingest it using Lesson 2's pipeline.

**Re-ingestion** — if stale files are detected:

```bash
# Re-run L2 pipeline for changed files
cd assets/02-powerup/pipeline/scripts
python ingest.py --source-dir ../../source-files
python convert.py
python chunking.py
python embed.py
```

---

## Done!

You've completed the full knowledge base lifecycle:

1. **Lesson 1:** Discovered client needs, audited content, generated KB files
2. **Lesson 2:** Indexed those files into a searchable vector database
3. **Lesson 3:** Deployed a live MCP server for Claude to search the KB, evaluated quality with Langfuse, and set up maintenance workflows

The "Project B" deliverable from Lesson 1 now has live semantic search. A client's team can ask Claude questions and get answers grounded in their actual knowledge base — with retrieval quality you can measure and improve.
