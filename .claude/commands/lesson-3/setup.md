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

Check if the student already has Supabase and OpenAI keys configured (e.g., from Lesson 2 or their Supabase MCP connection). If so, offer to reuse them.

Create a blank `assets/03-advanced/.env` with the key names below. Do NOT ask the user to paste secrets into the conversation — have them edit the file directly.

Point the user to these URLs to find their keys:

| Key | Where to find it | Format |
|-----|------------------|--------|
| `SUPABASE_URL` | Auto-detected from Supabase MCP `get_project_url` | `https://<ref>.supabase.co` |
| `SUPABASE_KEY` | https://supabase.com/dashboard/project/<PROJECT_ID>/settings/api → `service_role` secret | `eyJ...` (JWT, ~170 chars) |
| `OPENAI_API_KEY` | https://platform.openai.com/api-keys | `sk-...` |
| `LANGFUSE_PUBLIC_KEY` | https://us.cloud.langfuse.com/project/<PROJECT_ID>/settings/api-keys | `pk-lf-...` |
| `LANGFUSE_SECRET_KEY` | Same page as public key | `sk-lf-...` |

Pre-fill `SUPABASE_URL` if you can detect it. Pre-fill `LANGFUSE_BASE_URL` with the correct value. Leave all secret fields blank for the user to fill in.

```
SUPABASE_URL=<auto-detect from Supabase MCP if possible>
SUPABASE_KEY=
OPENAI_API_KEY=
LANGFUSE_PUBLIC_KEY=
LANGFUSE_SECRET_KEY=
LANGFUSE_BASE_URL="https://us.cloud.langfuse.com"
SETUP_COMPLETE=0
MCP_SERVER_READY=0
EVALUATION_COMPLETE=0
```

## Step 2b: Validate Connections

After the user has filled in their `.env`, verify each credential works before proceeding. Run these checks and report results as a pass/fail table:

1. **Supabase** — Use the Supabase MCP to run `SELECT 1` against the project. The project ID can be extracted from the SUPABASE_URL (the subdomain before `.supabase.co`).
2. **OpenAI** — Run a minimal embedding call to verify the API key:
   ```bash
   cd assets/03-advanced && python3 -c "
   from dotenv import load_dotenv; load_dotenv()
   import os, openai
   client = openai.OpenAI(api_key=os.environ['OPENAI_API_KEY'])
   r = client.embeddings.create(input='test', model='text-embedding-3-small')
   print(f'OpenAI OK — embedding dim: {len(r.data[0].embedding)}')
   "
   ```
3. **Langfuse** — Verify the keys authenticate:
   ```bash
   cd assets/03-advanced && python3 -c "
   from dotenv import load_dotenv; load_dotenv()
   import os
   from langfuse import Langfuse
   lf = Langfuse(
       public_key=os.environ['LANGFUSE_PUBLIC_KEY'],
       secret_key=os.environ['LANGFUSE_SECRET_KEY'],
       host=os.environ['LANGFUSE_BASE_URL']
   )
   lf.auth_check()
   print('Langfuse OK — authenticated')
   "
   ```

If any check fails, tell the user which key has the problem and link them back to the relevant URL from the Step 2 table. Do not proceed until all three pass.

## Step 3: Install Dependencies

**Critical version notes:**
- The MCP SDK (`@modelcontextprotocol/sdk ^1.0.0`) requires **Zod v3** for tool schema registration. Zod v4 is incompatible and will cause a silent startup failure. The `package.json` pins `zod: "^3.25.76"` — do not upgrade to v4.
- Python dependencies require a **virtual environment** on macOS (PEP 668). Create one at `assets/03-advanced/.venv` before installing.

```bash
# MCP server
cd assets/03-advanced/mcp-server && npm install

# Evaluation harness (use venv)
cd assets/03-advanced
python3 -m venv .venv
source .venv/bin/activate
pip install -r evaluation/requirements.txt
```

Add `.venv/` to `.gitignore` if not already present.

## Step 4: Apply Migration

Run `assets/03-advanced/migrations/004_create_query_log.sql` via Supabase MCP.

Verify:

```sql
SELECT count(*) FROM query_log;  -- Should return 0 (table exists, empty)
```

## Step 5: Configure MCP Server

Read the existing `.mcp.json` at the repo root (if it exists). Merge the `kb-search` entry into the `mcpServers` object. Do NOT overwrite other entries.

Before writing the config, compile the MCP server TypeScript to JavaScript:

```bash
cd assets/03-advanced/mcp-server && npx tsc
```

Verify `dist/index.js` exists after compilation.

The `kb-search` entry (uses compiled JS per MCP best practices — avoids npx/tsx startup issues):

**Important:** Use an absolute path in `args` — do NOT use a relative path with `cwd`. The `cwd` field can cause tools to silently fail to register despite the server connecting. Also ensure no trailing blank lines in the `env` block.

```json
{
  "command": "node",
  "args": ["/absolute/path/to/assets/03-advanced/mcp-server/dist/index.js"],
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
