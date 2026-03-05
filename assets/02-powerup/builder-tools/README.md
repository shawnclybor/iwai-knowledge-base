# Builder Tools

Core instructions for the RAG pipeline builder project. These files are project-agnostic — they work for any client, not just the Truepoint case study.

## Files

| File | Purpose | When to Read |
|------|---------|-------------|
| `instructions.md` | Step-by-step lesson workflow. Walks through the full pipeline: setup → ingest → chunk → embed → calibrate → review. | Read at session start or when picking up where you left off. |

The system prompt lives at the project root as `CLAUDE.md` (standard Claude Code convention). Lesson 1 used a `claude.md` here because it was designed for Claude Projects, which uses manually pasted instructions. Lesson 2 targets Claude Code/Cowork where `CLAUDE.md` auto-loads.

## How These Relate to Lesson 1

Lesson 1's builder tools focused on processing raw discovery materials (transcripts, audits, inventories) into static KB markdown files.

Lesson 2's builder tools focus on taking those KB files (or any document set) and making them searchable through a RAG pipeline — vector similarity search, full-text search, and hybrid retrieval backed by Supabase.

The two-project architecture still applies:
- **Project A (Builder):** Where the pipeline is configured and run. Builder tools + pipeline scripts live here.
- **Project B (Deliverable):** The client-facing project that queries the Supabase database for answers.
