# RAG Pipeline Plugin Definition

Single source of truth for the plugin: packaging instructions, MCP connector configs, and skill content.

## Plugin Anatomy

A Claude Code plugin is a zip file (`.plugin`) with this structure:

```
rag-pipeline-tools/
├── .claude-plugin/
│   └── plugin.json        # Manifest (name, version, what's inside)
├── .mcp.json               # MCP connectors (auto-start on install)
└── skills/                 # Slash commands
    ├── setup-rag/SKILL.md
    ├── ingest/SKILL.md
    └── calibrate/SKILL.md
```

Three parts, three jobs:
- **`plugin.json`** — identifies the plugin and declares its components
- **`.mcp.json`** — connects external services (Supabase) so they start automatically
- **`skills/`** — slash commands with YAML frontmatter (name, description, allowed-tools) + markdown instructions

That's it. Zip the folder, rename to `.plugin`, install.

## How to Package

Cowork only discovers skills through installed plugins. Package as a `.plugin` file and deliver via `present_files`.

### Step 1: Create plugin structure

```bash
mkdir -p /tmp/rag-pipeline-tools/.claude-plugin
mkdir -p /tmp/rag-pipeline-tools/skills/setup-rag
mkdir -p /tmp/rag-pipeline-tools/skills/ingest
mkdir -p /tmp/rag-pipeline-tools/skills/calibrate
```

### Step 2: Create the plugin manifest

```bash
cat > /tmp/rag-pipeline-tools/.claude-plugin/plugin.json << 'EOF'
{
  "name": "rag-pipeline-tools",
  "version": "0.2.0",
  "description": "RAG Pipeline Builder: skills (/setup-rag, /ingest, /calibrate) and Supabase MCP connector"
}
EOF
```

### Step 3: Create the MCP connector config

Claude Code auto-discovers `.mcp.json` at the plugin root — no need to reference it in `plugin.json`.

**Important:** Plugin `.mcp.json` does NOT use a `"mcpServers"` wrapper. Server names go directly at the root level. (This is different from project-scoped `.mcp.json` files, which do use the wrapper.)

Use `"type": "http"` for cloud services with remote MCP endpoints (renders with icon + Install button in Cowork).

```bash
cat > /tmp/rag-pipeline-tools/.mcp.json << 'EOF'
{
  "supabase": {
    "type": "http",
    "url": "https://mcp.supabase.com/mcp"
  }
}
EOF
```

Supabase uses remote HTTP with OAuth — no access token needed.

### Step 4: Write the SKILL.md files

Write each skill's content (from sections below) to the corresponding directory:
- `/tmp/rag-pipeline-tools/skills/setup-rag/SKILL.md` ← content from "Skill 1: setup-rag"
- `/tmp/rag-pipeline-tools/skills/ingest/SKILL.md` ← content from "Skill 2: ingest"
- `/tmp/rag-pipeline-tools/skills/calibrate/SKILL.md` ← content from "Skill 3: calibrate"

Each file must include the YAML frontmatter AND the markdown body exactly as written below.

### Step 5: Package and deliver

```bash
cd /tmp/rag-pipeline-tools && zip -r /tmp/rag-pipeline-tools.plugin . -x "*.DS_Store"
```

Copy the `.plugin` file to the user's workspace folder (the mounted mnt/ directory), then call `present_files` to deliver it. The user clicks to install it.

---

## Skill 1: setup-rag

```yaml
name: setup-rag
description: "Guided setup for the RAG pipeline. Walks through environment variables, Supabase migrations, MCP connectors, and Python dependencies."
allowed-tools: ["Bash", "Read", "Write", "Edit", "mcp__e54affaf-c4c2-4f1c-b89b-e67e6e697d58__execute_sql", "mcp__e54affaf-c4c2-4f1c-b89b-e67e6e697d58__apply_migration"]
```

### SKILL.md Content

```markdown
# Setup RAG Pipeline

Walk the user through setting up the RAG pipeline step by step. Check each prerequisite before moving on.

## Quick Check

Read `pipeline/scripts/.env`, then check phase flags and key state:

\`\`\`bash
cd pipeline/scripts && python -c "
from dotenv import load_dotenv; load_dotenv(); import os
for f in ['ENV_CONFIGURED','DEPS_INSTALLED','MIGRATIONS_APPLIED']:
    print(f'{f}:', os.environ.get(f, '0'))
for k in ['SUPABASE_URL','SUPABASE_KEY','OPENAI_API_KEY']:
    print(f'{k}:', 'set' if os.environ.get(k) else 'MISSING')
" 2>/dev/null || echo "No .env file"
\`\`\`

Skip to the first phase showing `0`. If keys are already set, Step 1 just needs verification + flag. If all phases show `1`, setup is done — suggest `/ingest`.

## Step 1: Environment Variables

The pipeline scripts need three env vars saved to `pipeline/scripts/.env` (persists between sessions). If the Quick Check showed keys already set, skip to the verification below. Otherwise, ask the user for their keys and write the file:

\`\`\`
SUPABASE_URL=https://<project-id>.supabase.co
SUPABASE_KEY=<service-role-key>
OPENAI_API_KEY=<openai-key>
\`\`\`

Where to find each value:
- `OPENAI_API_KEY` — from platform.openai.com/api-keys
- `SUPABASE_URL` — from Supabase dashboard → Settings → API → Project URL (or use the Supabase MCP `get_project_url` tool)
- `SUPABASE_KEY` — from Supabase dashboard → Settings → API → service_role key (not anon)

Verify all three load, then set the flag (run both — do NOT skip the flag):

\`\`\`bash
cd pipeline/scripts && python -c "from dotenv import load_dotenv; load_dotenv(); import os
missing = [k for k in ['OPENAI_API_KEY','SUPABASE_URL','SUPABASE_KEY'] if not os.environ.get(k)]
if missing: print('MISSING:', missing); exit(1)
print('All keys set')" && sed -i '/^ENV_CONFIGURED=/d' .env && echo "ENV_CONFIGURED=1" >> .env && echo "ENV_CONFIGURED done"
\`\`\`

## Step 2: Python Dependencies

\`\`\`bash
pip install --no-cache-dir -r pipeline/scripts/requirements.txt --break-system-packages
\`\`\`

Verify imports work, then set the flag (run both — do NOT skip the flag):

\`\`\`bash
cd pipeline/scripts && python -c "import dotenv, supabase, openai, tiktoken, docx, pdfplumber; print('All packages OK')" && sed -i '/^DEPS_INSTALLED=/d' .env && echo "DEPS_INSTALLED=1" >> .env && echo "DEPS_INSTALLED done"
\`\`\`

## Step 3: Supabase Migrations

Apply the three migration files in order. Read each file from `migrations/` and apply via the Supabase MCP `apply_migration` tool:

1. `001_create_file_metadata.sql`
2. `002_create_chunks.sql`
3. `003_create_rpc_functions.sql`

After each migration, confirm it succeeded. If `apply_migration` is unavailable, provide the SQL for the user to paste into the Supabase SQL Editor.

After all three succeed, set the flag (do NOT skip):

\`\`\`bash
cd pipeline/scripts && sed -i '/^MIGRATIONS_APPLIED=/d' .env && echo "MIGRATIONS_APPLIED=1" >> .env && echo "MIGRATIONS_APPLIED done"
\`\`\`

## Step 4: Verify MCP Connectors

Check that the Supabase MCP connector is working by running a simple query:

\`\`\`sql
SELECT count(*) FROM file_metadata;
\`\`\`

This should return 0 rows (empty table).

## Step 5: Source Files

Confirm the source files exist:

\`\`\`bash
ls -la source-files/
\`\`\`

Should show markdown, CSV, DOCX, and PDF files.

## Done

Tell the user:
- Setup is complete
- Next step: run `/ingest` to process the source files
```

---

## Skill 2: ingest

```yaml
name: ingest
description: "Run the RAG ingestion pipeline. Registers files, converts documents, chunks, embeds, and upserts to Supabase."
allowed-tools: ["Bash", "Read", "Write", "Supabase MCP tools"]
```

### SKILL.md Content

```markdown
# Ingest Pipeline

Run the full RAG pipeline to process source files into embedded chunks in Supabase.

## Quick Check

Check if ingestion was already completed in a previous session:

\`\`\`bash
cd pipeline/scripts && python -c "from dotenv import load_dotenv; load_dotenv(); import os; print('INGESTION_COMPLETE:', os.environ.get('INGESTION_COMPLETE', '0'))" 2>/dev/null || echo "INGESTION_COMPLETE: 0"
\`\`\`

If `INGESTION_COMPLETE: 1`, verify data is still there:

\`\`\`sql
SELECT count(*) as files FROM file_metadata WHERE status = 'completed';
SELECT count(*) as chunks FROM chunks WHERE embedding IS NOT NULL;
\`\`\`

If both return rows, tell the user ingestion is already done and suggest `/calibrate`. Otherwise, continue below.

## Arguments

`$ARGUMENTS` may contain:
- `--source-dir <path>` — override source folder (default: `source-files/`)
- `--dry-run` — embed but don't upsert to Supabase
- A specific filename to process just one file

## Pre-flight Checks

Before running, verify:
1. Environment variables are set (`OPENAI_API_KEY`, `SUPABASE_URL`, `SUPABASE_KEY`)
2. Supabase tables exist (run `SELECT count(*) FROM file_metadata;`)
3. Source files exist in the source directory

If any check fails, tell the user to run `/setup-rag` first.

**Note:** The `output/` directory is created automatically by the scripts — do not check for it or fail if it's missing.

## Stage 1: File Intake

Run the intake script to scan, hash, and register files:

\`\`\`bash
cd pipeline/scripts
python ingest.py --source-dir ../../source-files --output-dir ./output
\`\`\`

This outputs `registered.json` — a manifest of files that need processing.

## Stage 2: Document Conversion

\`\`\`bash
cd pipeline/scripts
python convert.py --input ./output/registered.json --output-dir ./output
\`\`\`

This converts each file to normalized markdown using lightweight Python libraries (python-docx for Word, pdfplumber for PDF, stdlib for CSV/MD). Output is saved to `output/converted.json`.

Tell the user how many files were converted and if any failed.

## Stage 3: Chunking

\`\`\`bash
cd pipeline/scripts
python chunking.py --input ./output/converted.json --output-dir ./output
\`\`\`

## Stage 4-5: Embedding and Upsert

\`\`\`bash
cd pipeline/scripts
python embed.py --input ./output/chunked.json
\`\`\`

If `$ARGUMENTS` contains `--dry-run`, add `--dry-run` to the `embed.py` command.

## Post-Pipeline Verification

After the pipeline completes, run these verification queries via Supabase MCP:

\`\`\`sql
-- File processing summary
SELECT status, count(*) FROM file_metadata GROUP BY status;

-- Chunk counts per file
SELECT f.file_name, f.chunk_count, f.chunk_strategy
FROM file_metadata f
WHERE f.status = 'completed'
ORDER BY f.file_name;

-- Total chunks
SELECT count(*) FROM chunks;
\`\`\`

Report the results to the user. If any files failed, show the error messages:

\`\`\`sql
SELECT file_name, error_message FROM file_metadata WHERE status = 'failed';
\`\`\`

## Cleanup

The intermediate JSON files in `pipeline/scripts/output/` can be deleted after a successful run, but mention they exist in case the user wants to inspect them.

If all files completed successfully (no failures), append the ingestion flag:

\`\`\`bash
cd pipeline/scripts && sed -i '/^INGESTION_COMPLETE=/d' .env && echo "INGESTION_COMPLETE=1" >> .env
\`\`\`
```

---

## Skill 3: calibrate

```yaml
name: calibrate
description: "Test retrieval quality with sample queries. Runs vector search, full-text search, and hybrid search against the chunks table and reports results."
allowed-tools: ["Bash", "Read", "mcp__e54affaf-c4c2-4f1c-b89b-e67e6e697d58__execute_sql"]
```

### SKILL.md Content

```markdown
# Calibrate RAG Retrieval

Test the quality of your embedded knowledge base by running sample queries against it.

## Arguments

`$ARGUMENTS` may contain:
- A specific query string to test (e.g., `"workers comp requirements in North Carolina"`)
- `--all` to run the full built-in test suite

If no arguments, run the full test suite.

## Pre-flight

Verify data exists:

\`\`\`sql
SELECT count(*) as total_chunks FROM chunks WHERE embedding IS NOT NULL;
\`\`\`

If 0, tell the user to run `/ingest` first.

## Test Suite

Run each test query using the `hybrid_search` RPC function. For each query:

1. Generate an embedding for the query text using the OpenAI API (text-embedding-3-small)
2. Call the `hybrid_search` function with that embedding

Since we can't call OpenAI from SQL directly, use Python:

\`\`\`bash
python -c "
import os, json
from openai import OpenAI
from supabase import create_client

client = OpenAI()
sb = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])

query = '\$QUERY'
resp = client.embeddings.create(model='text-embedding-3-small', input=[query])
embedding = resp.data[0].embedding

result = sb.rpc('hybrid_search', {
    'query_embedding': embedding,
    'query_text': query,
    'match_count': 5,
    'text_weight': 0.3,
    'vector_weight': 0.7
}).execute()

for r in result.data:
    print(f\"Score: {r['combined_score']:.3f} (vec:{r['vector_score']:.3f} txt:{r['text_score']:.3f}) | File: {r['file_name']}\")
    print(f\"  {r['content'][:150]}...\")
    print()
"
\`\`\`

### Built-in Test Queries

1. **"What are the workers compensation requirements in North Carolina?"**
   Expected: hits from workers-comp-state-reference.csv and handbook
2. **"How should we classify subcontractors vs employees?"**
   Expected: hits from subcontractor-classification-memo.md
3. **"What is the DOT drug testing policy for CDL drivers?"**
   Expected: hits from drug-testing-policy-dot.docx
4. **"What are the new overtime salary thresholds?"**
   Expected: hits from dol-overtime-rule-2024.pdf
5. **"FMLA eligibility requirements"**
   Expected: hits from fmla-policy-2023.md and handbook

## Report

After running all queries, summarize:
- Which queries returned relevant results in the top 3
- Which queries missed expected sources
- Whether full-text or semantic search is doing more of the heavy lifting
- Suggested weight adjustments if results seem off

## Tuning Tips

If results are poor:
- Try adjusting `text_weight` and `vector_weight` (they should sum to 1.0)
- Check if chunking produced meaningful sections (not too small, not too large)
- Verify embeddings are populated: `SELECT count(*) FROM chunks WHERE embedding IS NULL;`
```
