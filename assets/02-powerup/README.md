# Lesson 2: Power-Up — RAG Pipeline Integration

Build a retrieval-augmented generation pipeline that ingests knowledge base files into Supabase pgvector for semantic and hybrid search.

## What You'll Build

A pipeline that takes documents (markdown, Word, PDF, CSV), converts them to normalized text, chunks them intelligently, embeds them with OpenAI, and stores them in Supabase for vector similarity and full-text search.

## Prerequisites

- Completed Lesson 1 (Core) or familiarity with the knowledge base files
- Supabase account (free tier)
- OpenAI API key
- Claude Code or Cowork
- Python 3.10+

## Quick Start

```bash
# 1. Setup
/setup-rag

# 2. Ingest source files
/ingest

# 3. Test retrieval
/calibrate
```

## Folder Structure

```
02-powerup/
├── CLAUDE.md                    ← System prompt (Claude reads this on session start)
├── README.md                    ← You are here
├── lesson-flow.md               ← Visual diagram of the student journey
├── rag-pipeline-plan.md         ← Architecture and design decisions
├── RAG setup.png                ← Pipeline diagram (image)
│
├── .claude/                     ← Claude tooling
│   ├── README.md
│   ├── settings.json
│   ├── skill-definitions.md     ← All 3 skills + plugin packaging instructions
│   └── agents/
│       └── rag-reviewer.md      ← Quality review subagent
│
├── builder-tools/               ← Lesson workflow
│   ├── README.md
│   └── instructions.md          ← Step-by-step lesson workflow
│
├── migrations/                  ← Supabase schema
│   ├── README.md
│   ├── 001_create_file_metadata.sql
│   ├── 002_create_chunks.sql
│   └── 003_create_rpc_functions.sql
│
├── mcp-setup/                   ← MCP connector configuration
│   ├── README.md
│   └── mcp-connector-setup.md
│
├── pipeline/                    ← Pipeline templates and scripts
│   ├── README.md
│   ├── templates/               ← Step-by-step guides per stage
│   │   ├── file-intake.md
│   │   ├── docling-conversion.md
│   │   ├── chunking-router.md
│   │   ├── embedding.md
│   │   └── upsert.md
│   └── scripts/                 ← Ready-to-run Python scripts
│       ├── requirements.txt
│       ├── ingest.py            ← Stage 1: file intake
│       ├── convert.py           ← Stage 2: document conversion
│       ├── chunking.py          ← Stage 3: chunking router
│       └── embed.py             ← Stages 4-5: embedding + upsert
│
├── source-files/                ← Documents to ingest
│   ├── README.md
│   ├── handbook-nc-current.md
│   ├── anti-harassment-policy-2024.md
│   ├── fmla-policy-2023.md
│   ├── subcontractor-classification-memo.md
│   ├── onboarding-checklist-consultant.md
│   ├── workers-comp-state-reference.csv
│   ├── i9-audit-checklist.csv
│   ├── drug-testing-policy-dot.docx
│   ├── pto-policy-unlimited.docx
│   ├── dol-overtime-rule-2024.pdf
│   └── eeoc-harassment-guidance-2024.pdf
│
└── sample-files/                ← Expected outputs for verification
    ├── README.md
    ├── sample-query-results.md
    └── sample-calibration-report.md
```

## Tech Stack

| Component | Tool | Purpose |
|-----------|------|---------|
| Database | Supabase (pgvector) | Vector storage + full-text search |
| Embeddings | OpenAI text-embedding-3-small | 1536-dim semantic vectors |
| Conversion | python-docx, pypdf | File format normalization |
| Chunking | Custom Python | Per-type strategies (heading-based, row-group) |
| Search | Supabase RPC functions | Hybrid vector + full-text search |
| Tooling | Cowork plugin (skills + agents) | Guided setup, execution, and review |

## Pipeline Stages

1. **File Intake** — Scan, hash, dedup, register in file_metadata
2. **Conversion** — Convert all types to normalized markdown
3. **Chunking** — Split by headings (docs) or row-groups (CSV), ~600 tokens max
4. **Embedding** — Batch embed via OpenAI with rate limit handling
5. **Upsert** — Write to Supabase chunks table with transaction handling

## Two Approaches

This lesson supports two learning paths:

- **Guided path:** Follow the pipeline templates (`pipeline/templates/`) step by step, understanding each stage before running it
- **Fast path:** Run the Python scripts directly (`/ingest`) and inspect the results

Both produce the same output.
