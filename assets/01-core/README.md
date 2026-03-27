# Lesson 1: Core Workflow — Build the Knowledge

Transform raw discovery materials into structured, client-ready knowledge base files using Claude Projects.

## What You'll Build

A complete knowledge base for Truepoint HR Solutions: structured markdown files generated from stakeholder interviews and existing documents, packaged as a Claude Project the client can install and use immediately.

## Prerequisites

- Claude Pro account ($20/month) — free tier uses data for training, not suitable for client work
- Google Drive access to client materials (or use the sample files in this repo)
- Familiarity with markdown formatting

## Quick Start

1. Create a Claude Project and upload the builder tools from `builder-tools/`
2. Connect Google Drive via MCP
3. Follow `builder-tools/instructions.md` step by step

## The Case Study: Truepoint HR Solutions

Regional HR consulting firm in Charlotte, NC. 35 employees, ~120 clients, ~$3M revenue. Services include outsourced HR, compliance audits, handbook development, and recruiting support.

**Pain points driving this project:**
- Co-founder Lisa fields 12-15 internal questions/day, losing ~10 billable hours/week
- New consultants take 5-6 months to work independently
- 400+ templates in Google Drive with no version control
- Consultants spend ~20% of billable time answering the same recurring HR questions

## Key Concepts

**Knowledge base development has three stages:**
1. **Processing** — Clean, standardize, and structure raw materials (this lesson's focus)
2. **Retrieval** — Connect the KB to an LLM for search (Lesson 2)
3. **Generation** — LLM answers questions using retrieved context (Lesson 3)

**The two-project pattern:**
- **Builder Project** — Internal tool with reusable templates and MCP connectors. Processes raw materials into KB files. Client-agnostic.
- **Deliverable Project** — Client-facing Claude Project with KB files and a system prompt. Simple to install (upload files, paste instructions). No APIs or keys needed.

**KUAD classification:** Keep / Update / Archive / Delete — applied during the content audit to determine which documents to trust.

## Workflow (Estimated: ~1 Month)

| Week | Phase | What Happens |
|------|-------|-------------|
| 1 | Discovery | Stakeholder interviews, pain point mapping, scope definition |
| 2 | Content audit | Storage inventory, KUAD classification, gap analysis |
| 3 | Architecture | Organize KB files by domain, define system prompt, select connectors |
| 4 | Testing | Query testing, template validation, system prompt refinement |
| Final | Handoff | Live install session, SOP generation, retainer setup |

## Folder Structure

```
01-core/
├── README.md                    ← You are here
├── recordings/                  ← Session transcript
│   └── transcript.md
├── slides/                      ← Session slide deck (PDF)
│
├── builder-tools/               ← Uploaded to the Builder Project
│   ├── claude.md                ← System prompt
│   ├── instructions.md          ← Step-by-step workflow
│   ├── formatting-rules.md      ← KB file style guide
│   ├── dedupe-instructions.md   ← Conflict resolution rules
│   └── mcp-connector-setup.md   ← Connector configuration guide
│
├── templates/                   ← Processing templates (used in Step 2)
│   ├── transcript-processing.md
│   ├── storage-inventory.md
│   ├── content-audit.md
│   ├── recurring-questions.md
│   └── gap-list.md
│
├── raw-client-files/            ← Truepoint case study materials
│   ├── discovery-interview.txt
│   └── follow-up-interview.txt
│
└── sample-files/                ← Expected outputs for reference
```

## Tools and Templates

**Builder tools** (uploaded to Claude Project): `claude.md` (system prompt), `instructions.md` (workflow), `formatting-rules.md`, `dedupe-instructions.md`, `mcp-connector-setup.md`

**Processing templates** (used during Step 2): Storage inventory, content audit (KUAD), recurring questions, gap list. Each produces an intermediate artifact that feeds into KB file generation.

**Connectors:** Google Drive (required, read-only), Desktop Commander (optional, adds local file access), Zapier (optional, adds Drive write capability)

## Tech Stack

| Component | Tool | Cost |
|-----------|------|------|
| Platform | Claude Projects | $20-30/user/month |
| Connectors | Google Drive, Desktop Commander, Zapier | Free |
| **Total** | | **$20-30/month** |

## Pricing Context

Core implementations command **$3,000-$7,500**. Price depends on discovery scope, content volume, connector complexity, and training time. Roughly half the budget covers work around the technology (discovery, content development, training) rather than the build itself.

**Ongoing revenue:** $300-$5,000/month retainer for KB maintenance and updates.

## Common Mistakes

- **Overstuffing system instructions** — Keep the core prompt architectural. Move detailed instructions into separate KB files loaded on demand.
- **Skipping the two-project pattern** — Builder and deliverable stay separate. Raw materials accessed via connectors, not uploaded.
- **Not verifying sources** — Always ask the LLM to walk through where it found its information.
- **Using the free tier with client data** — Paid account required for client work.
- **Feature creep (YAGNI)** — Build what's needed, verify it works, then iterate.

## Platform Comparison

| Feature | Claude Projects | ChatGPT Projects | Gemini Gems |
|---------|----------------|-------------------|-------------|
| Connectors | Native + MCP | Native + MCP | Google Workspace only |
| Custom instructions | Project-level | Project-level | Gem instructions |
| KB files | Unlimited (30MB each) | 20-40 per project | 32 files or Drive refs |
| Best for | Deepest project integration | MS/Google storage teams | Google-only shops |

## What This Lesson Produces

The live demo generated seven KB files from two interview transcripts and sample documents in approximately one hour. The builder project is reusable across clients — only the raw materials and outputs change. The deliverable installation requires no technical knowledge from the client.

This is the foundation. Lesson 2 (Power-Up) indexes these files for semantic search. Lesson 3 (Advanced) deploys live retrieval with evaluation.
