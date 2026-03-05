# Claude Tooling — Lesson 2 (Power-Up)

This folder contains skill definitions, agents, and settings for the RAG pipeline lesson.

## Skills

All three skills are defined in `skill-definitions.md` (single source of truth). They are packaged as a Cowork plugin during the boot sequence in CLAUDE.md.

| Skill | Command | Purpose |
|-------|---------|---------|
| setup-rag | `/setup-rag` | Guided setup: env vars, migrations, MCP, dependencies |
| ingest | `/ingest` | Run the full pipeline: intake → convert → chunk → embed → upsert |
| calibrate | `/calibrate` | Test retrieval quality with sample queries |

## Agents

| Agent | Type | Purpose |
|-------|------|---------|
| rag-reviewer | Explore | Read-only quality review of pipeline output |

## Settings

`settings.json` pre-approves common pipeline commands so students don't get permission prompts during the lesson.

## How It Works

1. CLAUDE.md boot sequence detects missing skills in `<available_skills>`
2. Reads `skill-definitions.md` for packaging instructions + skill content
3. Builds a `.plugin` file and presents it to the user
4. User installs → skills appear as `/setup-rag`, `/ingest`, `/calibrate`
5. Lesson begins
