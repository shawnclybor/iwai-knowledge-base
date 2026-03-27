# IWAI Build it Together: Knowledge Bases

Lesson materials for IWAI's "Build it Together" (BiT) series on Knowledge Bases. The series teaches AI consultants how to build a Claude Project-based knowledge base for a client, using a fictional case study: **Truepoint HR Solutions** (Charlotte, NC — 35 employees, ~120 clients, ~$2.8M revenue, HR consulting).

Lesson slides live in each lesson's `slides/` directory. Session recordings and transcripts are in `recordings/`.

## Lessons

| Folder | Lesson | Status |
|--------|--------|--------|
| `00-intro/` | Introduction — background research, context-setting | Slides complete; research guide in repo |
| `01-core/` | Core Workflow — building a KB from raw client materials | Complete |
| `02-powerup/` | Power-Up — RAG pipeline integration | Complete |
| `03-advanced/` | Advanced — MCP server deployment + evaluation | Complete |

## Repo Structure

```
assets/
├── 00-intro/                        # Lesson 0: Introduction
│   └── knowledge_base_research_guide.md
├── 01-core/                         # Lesson 1: Core Workflow
│   ├── raw-client-files/            # True raw inputs (Truepoint-specific)
│   │   ├── stakeholder-interview-transcript-2025-01-13.txt
│   │   ├── stakeholder-followup-transcript-2025-01-20.txt
│   │   └── sample-client-files/     # 4 redacted industry samples
│   ├── builder-tools/               # Project-agnostic core instructions
│   │   ├── claude.md                # System prompt for builder project
│   │   ├── instructions.md          # Step-by-step builder workflow
│   │   ├── formatting-rules.md      # KB file style guide
│   │   ├── dedup-instructions.md    # Conflict resolution rules (7 rules)
│   │   └── mcp-connector-setup.md   # Cloud storage MCP config guide
│   ├── templates/                   # Project-agnostic processing templates
│   │   ├── transcript-processing.md # Step 2a: raw transcript → structured data
│   │   ├── storage-inventory.md     # Step 2b: Drive access → folder/file inventory
│   │   ├── content-audit.md         # Step 2c: inventory → KUAD-tagged audit
│   │   ├── recurring-questions.md   # Step 2d: transcripts → question list
│   │   └── gap-list.md             # Step 2e: questions + inventory → gap analysis
│   └── sample-files/                # Pre-built exemplars of template outputs
│       ├── test-storage-inventory.md
│       ├── test-content-audit.md
│       ├── test-recurring-questions.md
│       ├── test-gap-list.md
│       ├── test-transcript-discovery-2025-01-13.md
│       └── test-transcript-followup-2025-01-20.md
├── 02-powerup/                      # Lesson 2: Power-Up (RAG)
│   ├── README.md                    # Lesson overview + folder structure
│   ├── lesson-flow.md               # Visual student journey diagram
│   ├── rag-pipeline-plan.md         # Architecture decisions
│   ├── RAG setup.png                # Pipeline diagram (image)
│   ├── .claude/                     # Claude Code skills + agents
│   │   ├── skills/setup-rag/        # /setup-rag — guided setup
│   │   ├── skills/ingest/           # /ingest — run pipeline
│   │   ├── skills/calibrate/        # /calibrate — test retrieval
│   │   └── agents/rag-reviewer.md   # Quality review subagent
│   ├── builder-tools/               # Lesson workflow
│   │   └── instructions.md
│   ├── migrations/                  # Supabase schema (3 SQL files)
│   ├── mcp-setup/                   # MCP connector config
│   ├── pipeline/
│   │   ├── templates/               # Step-by-step guides (5 stages)
│   │   └── scripts/                 # Python scripts (ingest, chunk, embed)
│   ├── source-files/                # 11 files: md, csv, docx, pdf
│   └── sample-files/                # Expected outputs for verification
└── 03-advanced/                     # Lesson 3: Advanced (Go Live)
    ├── README.md                    # Lesson overview + prerequisites
    ├── lesson-flow.md               # Visual student journey diagram
    ├── builder-tools/
    │   └── instructions.md          # 7-step workflow
    ├── mcp-server/                  # TypeScript MCP server (stdio)
    │   ├── package.json
    │   ├── tsconfig.json
    │   └── src/
    │       ├── index.ts             # Entry point + startup validation
    │       ├── tools/
    │       │   ├── search-kb.ts     # search_kb: embed → search → rerank → log
    │       │   └── list-sources.ts  # list_sources: query file_metadata
    │       └── lib/
    │           └── supabase.ts      # Supabase + OpenAI client init
    ├── evaluation/                  # Python eval harness (Langfuse + Ragas)
    │   ├── requirements.txt
    │   ├── evaluate.py              # Runner: embed → search → generate → score
    │   └── datasets/
    │       └── truepoint-queries.json  # 15 test queries
    ├── migrations/
    │   └── 004_create_query_log.sql # query_log table + RLS
    ├── templates/                   # Stage-specific briefings
    │   ├── mcp-server-build.md      # Read before /lesson-3:setup
    │   ├── evaluation-harness.md    # Read before /lesson-3:evaluate
    │   └── maintenance-ops.md       # Read before /lesson-3:maintain
    └── sample-files/
        ├── sample-search-results.md
        └── sample-evaluation-report.md

.claude/
├── commands/
│   ├── lesson-3/
│   │   ├── setup.md                 # /lesson-3:setup
│   │   ├── evaluate.md              # /lesson-3:evaluate
│   │   └── maintain.md              # /lesson-3:maintain
│   └── process-transcript.md       # /process-transcript
├── agents/
│   ├── kb-auditor.md                # Quality audit agent
│   └── transcript-processor.md     # Raw transcript → lesson notes
└── settings.json                    # Shared settings (no secrets)

.mcp.json                            # MCP server config (supabase)
```

## The Build → Index → Deploy Arc

Each lesson builds on the previous one, progressing the same case study from raw materials to a live, measurable knowledge base.

### Lesson 1: Core Workflow — Build the Knowledge

Process raw discovery materials (stakeholder interviews, client documents) into structured, client-ready KB files using Claude Projects. Uses a **two-project pattern**: a reusable Builder Project (templates + MCP connectors) and a simple Deliverable Project (KB files + system prompt) the client installs.

**Workflow:** Locate materials → process transcripts → inventory storage → audit content (KUAD) → compile questions → identify gaps → generate KB files → handoff

**Deliverable:** 5-10 structured markdown KB files. **Price range:** $3K-$7.5K.

See `assets/01-core/README.md` for full details.

### Lesson 2: Power-Up — Index the Knowledge

Ingest L1's KB files into a Supabase vector database via a 5-stage RAG pipeline. Uses Claude Cowork with custom skills (`/setup-rag`, `/ingest`, `/calibrate`).

**Pipeline:** File intake → conversion → chunking → embedding (OpenAI) → upsert to Supabase

**Deliverable:** Searchable vector DB with `hybrid_search()` and `match_chunks()` RPCs. **Price range:** $8K-$25K.

See `assets/02-powerup/README.md` for full details.

### Lesson 3: Advanced — Deploy the Knowledge

Wire Claude Code to Supabase for live search via a custom MCP server, connect evaluation tooling (Langfuse + Ragas), run tests, and establish an iteration loop for ongoing maintenance.

**Flow:** Set up tooling → run live queries → evaluate with test harness → iterate (find problems → diagnose → fix → re-test)

**Deliverable:** Running MCP server + evaluation baseline + maintenance workflow. **Price range:** $25K-$200K+.

See `assets/03-advanced/README.md` for full details.
