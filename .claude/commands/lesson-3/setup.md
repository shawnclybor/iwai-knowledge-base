---
description: "Set up Lesson 3: prerequisites, env vars, deps, migration, MCP server deploy"
---

# Lesson 3 Setup

Run all setup steps for Lesson 3. Checks prerequisites, configures environment, installs dependencies, applies migration, and deploys the MCP server.

## Before You Start

Read these for background on what you're building:
- `assets/03-advanced/templates/mcp-server-build.md` — What MCP servers are and how kb-search works
- `assets/03-advanced/templates/search-and-rpc.md` — How search, RPC, hybrid search, and query logging work

## Step 1: Check Prerequisites

Check these in order. Stop at the first failure.

```bash
node --version   # Must be >= 18
python --version # Must be >= 3.10
```

If Node.js is missing or < 18, tell the student: "Node.js 18+ is required for the MCP server. Install it from https://nodejs.org/"

Verify Lesson 2 is complete by querying Supabase (use the Supabase MCP):

```sql
-- All 4 checks must pass
SELECT count(*) FROM chunks WHERE embedding IS NOT NULL;           -- Must be > 0
SELECT count(*) FROM file_metadata WHERE status = 'completed';    -- Must be > 0
SELECT proname FROM pg_proc WHERE proname = 'hybrid_search';      -- Must return 1 row
SELECT proname FROM pg_proc WHERE proname = 'match_chunks';       -- Must return 1 row
```

If any check fails: "Lesson 2 must be completed first. The knowledge base needs to be indexed before it can be deployed."

## Step 1b: Validate KB Health

Run the `kb-auditor` agent to perform a comprehensive quality check on the Lesson 2 output. This verifies database health, chunk quality, and search readiness before building on top of it.

The auditor will report:
- File processing status (all files should be `completed`)
- Chunk quality (token distribution, outliers)
- Search readiness (RPC functions exist, indexes healthy)

If the auditor reports CRITICAL issues, resolve them before continuing. NEEDS ATTENTION items can be noted and addressed later.

## Step 2: Environment Variables

Check if Lesson 2's `.env` exists at `assets/02-powerup/pipeline/scripts/.env`. If it does, offer to reuse the Supabase and OpenAI keys.

Collect all required values and write to `assets/03-advanced/.env`:

```
SUPABASE_URL=<from L2 or ask>
SUPABASE_KEY=<from L2 or ask — must be service role key>
OPENAI_API_KEY=<from L2 or ask>
LANGFUSE_PUBLIC_KEY=<ask — sign up at https://langfuse.com, go to Settings → API Keys>
LANGFUSE_SECRET_KEY=<ask>
LANGFUSE_HOST=https://cloud.langfuse.com
SETUP_COMPLETE=0
MCP_SERVER_READY=0
EVALUATION_COMPLETE=0
```

## Step 3: Install Dependencies

```bash
# MCP server
cd assets/03-advanced/mcp-server && npm install

# Evaluation harness
pip install -r assets/03-advanced/evaluation/requirements.txt
```

## Step 4: Apply Migration

Run `assets/03-advanced/migrations/004_create_query_log.sql` via Supabase MCP.

Verify:

```sql
SELECT count(*) FROM query_log;  -- Should return 0 (table exists, empty)
```

## Step 5: Configure MCP Server

Read the existing `.mcp.json` at the repo root (if it exists). Merge the `kb-search` entry into the `mcpServers` object. Do NOT overwrite other entries.

The `kb-search` entry:

```json
{
  "command": "npx",
  "args": ["tsx", "src/index.ts"],
  "cwd": "assets/03-advanced/mcp-server",
  "env": {
    "SUPABASE_URL": "<actual value from .env>",
    "SUPABASE_KEY": "<actual value from .env>",
    "OPENAI_API_KEY": "<actual value from .env>"
  }
}
```

Also ensure a `supabase` entry exists:

```json
{
  "type": "http",
  "url": "https://mcp.supabase.com/mcp"
}
```

Write the merged `.mcp.json` to the repo root.

## Step 6: Set Flag and Restart

Update `assets/03-advanced/.env`: set `SETUP_COMPLETE=1`.

Tell the student: **"Setup complete. Restart Claude Code to load the new MCP server. Then say 'continue' and I'll verify the tools are available."**

When the student returns after restart, check that the `search_kb` and `list_sources` tools are available from the `kb-search` MCP server. If they are, set `MCP_SERVER_READY=1`.

Then run a quick test: call `list_sources` to verify the server connects to Supabase and returns the file list.
