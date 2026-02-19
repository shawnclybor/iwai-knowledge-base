# Builder Workflow

This file contains the step-by-step process for transforming raw discovery materials into structured knowledge base files.

---

## Getting Started

When a consultant starts a conversation, introduce yourself briefly and ask what they need. Do not search storage or start processing until you know the context.

**Ask what they need:**
1. **Project setup** — first time using this builder project, need to connect storage and verify access
2. **New client** — starting a fresh KB build for a client
3. **Existing client** — picking up where we left off on a client already in progress
4. **Isolated task** — processing a single file, resolving a conflict, or other one-off work

For options 2–4, ask the client's name, where their files are stored, and where generated files should be saved (Google Drive folder or local computer).

---

## Step 1: Locate Raw Materials

Search the client's storage for the raw discovery materials. These are the starting inputs — everything else gets built from them.

**What to look for:**

- **Stakeholder interview transcripts** — Raw recordings or transcriptions from discovery sessions (Otter.ai, manual, etc.)
- **Sample client-facing documents** — Templates, policies, handbooks, and other operational files pulled from the client's storage
- **Storage access** — MCP connector to the client's Drive/SharePoint, or screenshots/exports of the folder structure

List what you find. If raw transcripts or storage access are missing, tell the consultant — these are required before proceeding. Sample documents are helpful but not blocking.

**Also check for previously processed materials.** If the consultant has already done some processing (from a prior session or manually), look for:

- Processed transcripts
- Storage inventories
- Content audits (KUAD-tagged)
- Recurring question lists
- Gap analyses

If any of these exist and are current, verify them and skip the corresponding processing step in Step 2.

---

## Step 2: Process Discovery Materials

Work through the raw materials in sequence. Each step builds on the previous one. Use the corresponding template for each.

### 2a. Process Transcripts

**Template:** `transcript-processing.md`
**Input:** Raw interview/meeting transcripts
**Output:** Structured data — pain points, workflows, quotes, gaps, priorities

Process each transcript into the structured format defined in the template. Follow the file naming convention — note that the transcript date may be embedded in the file name itself. Save each processed transcript to the designated save location. These processed transcripts feed every downstream step.

### 2b. Document Storage

**Template:** `storage-inventory.md`
**Input:** MCP access to client's storage, or screenshots/exports
**Output:** Structured inventory of the client's folder and file structure with auditor notes

Walk the client's storage and produce a complete inventory. If the consultant already has a file/folder listing, format it using the template. Save the inventory to the designated save location.

### 2c. Audit Content

**Template:** `content-audit.md`
**Input:** Storage inventory + processed transcripts + access to documents
**Output:** KUAD-tagged assessment of every relevant document (Keep / Update / Archive / Delete)

Review each document found in the storage inventory and assign a KUAD tag with reasoning. Use stakeholder comments from the transcripts to inform tags. Save the content audit to the designated save location. This audit governs which documents the builder trusts during KB generation (see `dedup-instructions.md`, Rule 1).

### 2d. Compile Recurring Questions

**Template:** `recurring-questions.md`
**Input:** Processed transcripts
**Output:** Categorized list of questions the client's team asks repeatedly

Extract and categorize the recurring internal questions from the processed transcripts. Save the question list to the designated save location. This list feeds directly into the gap analysis.

### 2e. Identify Knowledge Gaps

**Template:** `gap-list.md`
**Input:** Recurring questions list + storage inventory + content audit
**Output:** Structured gap list with impact assessment and recommended KB files

Cross-reference the recurring questions against the storage inventory and content audit to identify what's missing, outdated, or unfindable. Each gap gets an impact rating and a recommended KB file. Save the gap list to the designated save location.

---

## Step 3: Source Assessment

Review all processed materials and produce a **source assessment**:

- **Client overview:** Who is the client? What do they do? (Pull from processed transcripts and inventories)
- **Core problems:** What pain points is the knowledge base solving? (Pull from transcripts, question lists, gap analyses)
- **Proposed workflows:** What workflows should the deliverable Claude Project support? (Infer from recurring questions, pain points, and stakeholder priorities)
- **Proposed KB files:** A list of KB files to generate, grouped by workflow, with the primary source files each will draw from
- **Primary home assignments:** A table mapping key topics to their primary KB file to prevent duplication (see `dedup-instructions.md`, Rule 4)

Present this plan and **wait for approval** before generating any files.

---

## Step 4: Generate KB Files

For each approved KB file:

1. Read the primary source files from the connected storage
2. Apply `formatting-rules.md` for structure, metadata, and citations
3. Apply `dedup-instructions.md` to resolve any conflicts across sources
4. Produce the complete file content
5. Save the file to the designated save location
6. Provide a brief generation summary: sources used, gaps flagged, dedup decisions made

Generate one file at a time unless asked to batch. After each file, confirm it was saved and ask if the consultant wants to revise before moving to the next.

---

## Step 5: Review and Handoff

After all KB files are generated, provide a **completion summary**:

- Total KB files generated, grouped by workflow
- All content gaps flagged across the files (consolidated list)
- All dedup decisions made (consolidated list)
- Recommended next steps: what the consultant needs to do to set up the deliverable Claude Project (Project B), including which generated KB files to upload and that a separate client-facing claude.md will be needed
