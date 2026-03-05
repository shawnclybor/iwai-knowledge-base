# Pipeline

The RAG ingestion pipeline converts source documents into embedded, searchable chunks stored in Supabase.

## Two Ways to Build

This folder contains both **templates** (guided build) and **scripts** (ready-to-run reference). Use whichever approach fits your learning style:

| Approach | Folder | How It Works |
|----------|--------|-------------|
| **Guided build** | `templates/` | Step-by-step instructions. Claude reads each template and helps you build the pipeline piece by piece. |
| **Reference scripts** | `scripts/` | Complete Python scripts you can run directly. Use these to check your work or skip ahead. |

## Pipeline Stages

```
Source Files → File Intake → Document Conversion → Chunking → Embedding → Supabase
```

| Stage | Template | Script | What It Does |
|-------|----------|--------|-------------|
| 1. File Intake | `file-intake.md` | `ingest.py` | Scan source folder, compute SHA256 hash, dedup check, insert file_metadata row |
| 2. Document Conversion | `docling-conversion.md` | `convert.py` | Convert each file to normalized markdown (python-docx, pdfplumber) |
| 3. Chunking | `chunking-router.md` | `chunking.py` | Analyze document structure, select strategy per file type, generate chunks |
| 4. Embedding | `embedding.md` | `embed.py` | Batch embed chunks with OpenAI text-embedding-3-small (1536d) |
| 5. Upsert | `upsert.md` | `embed.py` | Batch insert chunks + embeddings into Supabase, update file_metadata status |

## Prerequisites

- Supabase MCP connected (see `../mcp-setup/`)
- Migrations applied (see `../migrations/`)
- OpenAI API key set as environment variable: `export OPENAI_API_KEY=sk-...`
- Python dependencies installed: `pip install -r scripts/requirements.txt`
