# Lesson 2: Power-Up — Index the Knowledge

Build a RAG pipeline that ingests Lesson 1's knowledge base files into Supabase pgvector for semantic and hybrid search.

## What You'll Build

A pipeline that takes documents (markdown, Word, PDF, CSV), converts them to normalized text, chunks them intelligently, embeds them with OpenAI, and stores them in Supabase for vector similarity and full-text search.

## Prerequisites

- Completed Lesson 1 (Core) or familiarity with the KB files
- Supabase account (free tier)
- OpenAI API key
- Claude Code or Cowork
- Python 3.10+

## Quick Start

```bash
/setup-rag    # Environment, dependencies, migrations
/ingest       # Run the full pipeline
/calibrate    # Test retrieval quality
```

## Key Concepts

**Retrieval-Augmented Generation (RAG):** Instead of dumping documents into an LLM context window, RAG embeds them as vectors, retrieves only the relevant chunks for each query, and passes those to the LLM for answer generation. More accurate, less token waste.

**Embeddings:** Numerical representations of text that capture semantic meaning. "Cat," "kitten," and "feline" cluster together on a vector map even though they differ as keywords. This is the difference between keyword search and semantic search.

**Chunking:** Breaking documents into smaller pieces for embedding. Strategy matters — the pipeline uses heading-based splits for structured docs, row-group splits for CSVs, and whole-document for small files. Target: ~600 tokens per chunk.

**Hybrid search:** Combines vector similarity (70% weight) with keyword matching (30% weight). Vector search handles conceptual queries; keyword search catches exact terms like "FMLA" or "DOT." Weights are tunable during calibration.

## Pipeline Stages

1. **File Intake** — Scan, hash (SHA256), dedup, register in `file_metadata`
2. **Conversion** — Convert all formats to normalized markdown (python-docx, pypdf)
3. **Chunking** — Split by headings or row-groups using document anchors
4. **Embedding** — Batch embed via OpenAI text-embedding-3-small (1536 dims)
5. **Upsert** — Write chunks + vectors to Supabase with full-text index (tsvector)

The live demo processed 12 files into 89 chunks with zero failures.

## Folder Structure

```
02-powerup/
├── CLAUDE.md                    ← System prompt + boot sequence
├── README.md                    ← You are here
├── recordings/                  ← Session transcript
│   └── transcript.md
├── slides/                      ← Session slide deck (PDF)
│
├── builder-tools/               ← Lesson workflow
│   └── instructions.md
│
├── migrations/                  ← Supabase schema (3 migrations)
│   ├── 001_create_file_metadata.sql
│   ├── 002_create_chunks.sql
│   └── 003_create_rpc_functions.sql
│
├── pipeline/
│   ├── templates/               ← Stage-by-stage learning guides
│   │   ├── file-intake.md
│   │   ├── docling-conversion.md
│   │   ├── chunking-router.md
│   │   ├── embedding.md
│   │   └── upsert.md
│   └── scripts/                 ← Ready-to-run Python scripts
│       ├── ingest.py, convert.py, chunking.py, embed.py
│       └── requirements.txt
│
├── source-files/                ← 11 documents in 4 formats (md, csv, docx, pdf)
└── sample-files/                ← Expected outputs for verification
```

## Tech Stack

| Component | Tool | Purpose |
|-----------|------|---------|
| Database | Supabase (pgvector) | Vector storage + full-text search |
| Embeddings | OpenAI text-embedding-3-small | 1536-dim semantic vectors |
| Conversion | python-docx, pypdf | File format normalization |
| Chunking | Custom Python | Per-type strategies (heading-based, row-group) |
| Search | Supabase RPC functions | `hybrid_search()` + `match_chunks()` |
| Tooling | Cowork plugin | Skills (`/setup-rag`, `/ingest`, `/calibrate`) + agents |

## Two Learning Paths

- **Guided:** Follow pipeline templates step by step, understand each stage before running it
- **Fast:** Run `/ingest` directly and inspect results

Both produce the same output.

## Skills

| Skill | What It Does |
|-------|-------------|
| `/setup-rag` | Environment vars, dependencies, migrations, MCP connector |
| `/ingest` | Full pipeline: intake → convert → chunk → embed → upsert |
| `/calibrate` | Test queries against the KB, verify retrieval accuracy |

Skills track progress via `.env` flags (`ENV_CONFIGURED`, `DEPS_INSTALLED`, `MIGRATIONS_APPLIED`, `INGESTION_COMPLETE`) and resume where you left off across sessions.

## Operational Costs

| Service | Cost | Notes |
|---------|------|-------|
| Claude Pro | $20/month | Required for Cowork |
| Supabase | $0-25/month | Free tier: 500MB storage; $10/project on paid |
| OpenAI embeddings | ~$5-20 one-time, ~$0.50/month | text-embedding-3-small |
| **Total** | **Under $100/month** | |

## Pricing Context

Power-Up implementations command **$8,000-$25,000**. A straightforward deployment falls in the $8K-$10K range. The KB is portable — once in Supabase, it connects to Zapier, n8n, Flowise, Vapi, or any tool with a Supabase integration.

## Troubleshooting

- **Wrong Supabase project ID** — Claude may pick the wrong project. Verify the project ref matches your target.
- **MCP connector not recognized** — Restart the app (Cmd-Q, relaunch) after installing.
- **RLS security warnings** — Enable RLS with no policies to satisfy warnings while keeping service role access.
- **Model selection** — Opus is token-heavy. Switch to Sonnet for pipeline stages if hitting usage limits.
- **Low retrieval scores** — Add keyword metadata tags to chunks. Consider skipping embedding for structured data (CSV) and querying it via SQL instead.

## Architecture Flexibility

Every component is swappable: embedding provider (Cohere, Voyage AI), vector database (Pinecone, Qdrant, Chroma), document processing (Docling, Unstructured.io), LLM platform. The MCP integration layer makes mixing components straightforward.

## What This Lesson Produces

A Supabase database with `file_metadata` (12 files tracked) and `chunks` (89 embedded chunks) tables, plus `hybrid_search()` and `match_chunks()` RPC functions. The KB is now searchable — but only via SQL. Lesson 3 (Advanced) wires this up so Claude can search it directly and evaluates retrieval quality.
