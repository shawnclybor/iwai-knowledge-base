# Lesson 2: Power-Up — Student Journey

```
┌─────────────────────────────────────────────────────────────────┐
│                    LESSON 2: RAG PIPELINE                       │
│                                                                 │
│  Student clones repo → Opens in Claude Code / Cowork            │
│  Follows video step-by-step                                     │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 1: SETUP                                     /setup-rag  │
│  ├── Set environment variables (OpenAI, Supabase)               │
│  ├── Install Python dependencies                                │
│  ├── Apply 3 SQL migrations to Supabase                         │
│  │    ├── 001: file_metadata table                              │
│  │    ├── 002: chunks table + pgvector + indexes                │
│  │    └── 003: match_chunks + hybrid_search RPCs                │
│  └── Verify MCP connectors                                      │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 2: REVIEW SOURCE FILES                                    │
│  ├── 5 markdown files (handbook, policies, memos, checklists)   │
│  ├── 2 CSV files (workers comp, I-9 audit)                      │
│  ├── 2 DOCX files (drug testing, PTO policy)                    │
│  └── 2 PDF files (DOL overtime, EEOC harassment guidance)       │
│       11 files total — all 4 file types represented             │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 3: RUN PIPELINE                                 /ingest   │
│                                                                 │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌─────────────┐  │
│  │ Stage 1  │──▶│ Stage 2  │──▶│ Stage 3  │──▶│ Stage 4-5   │  │
│  │ Intake   │   │ Convert  │   │ Chunk    │   │ Embed+Upsert│  │
│  └──────────┘   └──────────┘   └──────────┘   └─────────────┘  │
│                                                                 │
│  ingest.py          ingest.py      chunking.py     embed.py     │
│  ┌────────────┐  ┌────────────┐  ┌───────────┐  ┌───────────┐  │
│  │Scan folder │  │md: pass-   │  │md/docx/pdf│  │OpenAI API │  │
│  │SHA256 hash │  │  through   │  │ heading-  │  │ batch     │  │
│  │Dedup check │  │csv: table  │  │ based     │  │ embed     │  │
│  │Register in │  │  format    │  │csv: row-  │  │Supabase   │  │
│  │ Supabase   │  │docx: python│  │ group     │  │ upsert    │  │
│  │            │  │  -docx     │  │~600 tokens│  │1536 dims  │  │
│  │            │  │pdf: pypdf  │  │ per chunk │  │           │  │
│  └────────────┘  └────────────┘  └───────────┘  └───────────┘  │
│                                                                 │
│  Output: converted.json → chunked.json → Supabase chunks table  │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 4: VERIFY + CALIBRATE                       /calibrate   │
│  ├── Check file_metadata: all files status = 'completed'        │
│  ├── Check chunks: correct counts, no nulls                     │
│  ├── Test full-text search (tsvector)                           │
│  ├── Test vector similarity search (pgvector HNSW)              │
│  └── Test hybrid search with weight tuning                      │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 5: QUALITY REVIEW (OPTIONAL)          rag-reviewer agent  │
│  ├── Database health check                                      │
│  ├── Chunk quality analysis (token distribution)                │
│  ├── Metadata completeness                                      │
│  └── Search readiness verification                              │
└─────────────────────────────────────────────────────────────────┘
```

## Architecture Overview

```
Source Files (repo)          Supabase (pgvector)
┌────────────────┐           ┌──────────────────────────────┐
│ *.md           │           │ file_metadata                │
│ *.csv          │──ingest──▶│   id, file_name, file_hash,  │
│ *.docx         │  .py      │   status, chunk_count, ...   │
│ *.pdf          │           ├──────────────────────────────┤
└────────────────┘           │ chunks                       │
                             │   id, file_id, content,      │
   OpenAI API                │   embedding (vector 1536),   │
┌────────────────┐           │   content_tsv (tsvector),    │
│ text-embedding │──embed───▶│   chunk_metadata (jsonb)     │
│ -3-small       │  .py      ├──────────────────────────────┤
└────────────────┘           │ RPC Functions                │
                             │   match_chunks()             │
   Claude Code               │   hybrid_search()            │
┌────────────────┐           └──────────┬───────────────────┘
│ /setup-rag     │                      │
│ /ingest        │──────queries────────▶│
│ /calibrate     │◀─────results─────────│
│ rag-reviewer   │                      │
└────────────────┘
```

## File Type → Pipeline Path

| File Type | Converter | Chunking Strategy | Example File |
|-----------|-----------|-------------------|-------------|
| `.md` | Pass-through | Heading-based split | handbook-nc-current.md |
| `.csv` | Markdown table | Row-group (10 rows) | workers-comp-state-reference.csv |
| `.docx` | python-docx | Heading-based split | drug-testing-policy-dot.docx |
| `.pdf` | pypdf | Heading-based split | dol-overtime-rule-2024.pdf |
