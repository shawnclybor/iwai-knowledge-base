# CLAUDE.md

## Methodology

**Critical to ALWAYS FOLLOW**

- **KISS** — Keep it simple. Prefer the simplest solution that works. Don't over-engineer.
- **YAGNI** — You aren't gonna need it. Don't build for hypothetical future requirements.
- **5 Whys** — When debugging, ask "why" repeatedly to find the root cause before applying a fix.

See `README.md` for project overview, lesson structure, and repo layout.

## Key Concepts

- **KUAD tagging:** Keep/Update/Archive/Delete classification applied during the content audit step (2c) to determine which documents to trust during KB generation
- **Builder tools are agnostic:** All files in `builder-tools/` and `templates/` contain no Truepoint-specific references — they're reusable across any client engagement
- **Raw client files are Truepoint-specific:** The transcripts and sample files are written for the Truepoint case study
- **MCP is required for the builder project:** The builder project accesses raw client materials through MCP — nothing is uploaded except the builder tools and templates. MCP is read-only: for pulling file contents during processing, not for organizing or modifying Drive
- **Templates produce intermediate outputs:** The processing templates (Step 2a–2e) generate intermediate files in conversation (inventories, audits, question lists, gap analyses) that feed into KB file generation

## File Conventions

- All KB output files use markdown (`.md`)
- All intermediate outputs (inventories, audits, question lists, gap analyses) are markdown
- The stakeholder interview transcripts use Otter.ai format (`.txt`) with named speakers
- Sample client files include "Document Notes" sections tracing template sources and auditor flags

## What's Still Needed

### Lesson 1 (Core)

- **Deliverable KB files** — Run raw files through builder tools to generate ~10 KB files across 3 workflows
- **`deliverables/` folder** — Create `01-core/deliverables/` to hold generated KB files
- **Second claude.md** — Client-facing system prompt for the deliverable project (Project B)
- **Shared assets** — Master claude.md template, style guide, test query bank (20-30 questions per workflow), content update protocol

### Lesson 2 (Power-Up)

- Additional RAG-related lesson materials beyond the existing plan and diagram

### Lesson 3 (Advanced)

- Not yet scoped
