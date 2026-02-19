# Content Audit

Use this template to assess and tag every relevant document identified in the storage inventory. The output is a KUAD-tagged audit that tells the builder which documents to trust, which need updating, and which to ignore during KB generation.

---

## When to Use

Use this template after completing the storage inventory. The content audit reviews each document found in the inventory and assigns a status tag that governs how it's used in all downstream steps (see `dedup-instructions.md`, Rule 1).

---

## Required Inputs

- **Storage inventory** — The completed output from `storage-inventory.md`. Provides the file list to audit.
- **Processed transcripts** (recommended) — Stakeholder comments about document quality, currency, and reliability help inform KUAD tags.
- **Access to the documents themselves** (recommended) — Via MCP connector, to verify content, dates, and quality directly.

---

## KUAD Tags

Assign one tag to each document:

- **Keep** — Current, accurate, and in active use. This is the canonical version. Use its content directly during KB generation.
- **Update** — Contains valuable content but needs revision (outdated information, missing sections, wrong state-specific details). Use the content but flag specific items that need updating.
- **Archive** — Superseded by a newer version or no longer reflects current practice. Do not use during KB generation. Reference the Keep version instead.
- **Delete** — Duplicate, erroneous, mislabeled, or obsolete. Ignore completely. Do not reference in any KB file.

---

## How to Assess

For each document in the storage inventory's key folders:

1. **Check what stakeholders said.** If a transcript mentions that a specific document is outdated, wrong, or "the one we actually use," that's strong evidence.
2. **Check modification dates.** More recent generally wins, but not always — a well-maintained 2021 file may be better than a 2023 file that was never reviewed.
3. **Check for duplicates.** When multiple versions exist, identify the canonical one (Keep) and tag the rest (Archive or Delete).
4. **Check content quality.** Open the document if possible. Does it contain accurate information? Is it complete? Does it match what stakeholders described?
5. **When in doubt, tag as Update.** Better to flag something for review than to silently keep or archive it.

---

## Output Format

Produce a single markdown file:

```
# [Client Name] — Content Audit

*Document-level assessment of files found in the storage inventory. Each file is tagged Keep / Update / Archive / Delete to govern how it's used during knowledge base generation.*

**Audit date:** [YYYY-MM-DD — use the date this audit is performed]
**Storage inventory used:** [filename of the storage inventory this audit is based on]
**Transcripts used:** [filenames of processed transcripts used to inform KUAD tags]
**Auditor:** [Consultant name]

---

## KUAD Legend

| Tag | Meaning | How it's used in KB generation |
|---|---|---|
| **Keep** | Current and accurate | Use content directly |
| **Update** | Valuable but needs revision | Use content, flag items needing update |
| **Archive** | Superseded or outdated | Do not use; reference Keep version instead |
| **Delete** | Duplicate, erroneous, or obsolete | Ignore completely |

---

## [Folder Name]

| File | KUAD | Reasoning | Notes |
|---|---|---|---|
| [filename.ext] | Keep | [Why — e.g., "confirmed current by Lisa in discovery interview"] | [Any additional context] |
| [filename.ext] | Update | [Why — e.g., "contains 2022 minimum wage rates"] | [What specifically needs updating] |
| [filename.ext] | Archive | [Why — e.g., "superseded by version in HR Templates 2023/"] | [Which file supersedes it] |
| [filename.ext] | Delete | [Why — e.g., "exact duplicate of file in Client Templates/"] | |

---

[Repeat for each folder from the storage inventory that contains documents relevant to the knowledge base.]

---

## Summary

| Tag | Count | Percentage |
|---|---|---|
| Keep | [#] | [%] |
| Update | [#] | [%] |
| Archive | [#] | [%] |
| Delete | [#] | [%] |
| **Total audited** | [#] | 100% |

---

## Key Findings

- [Summary observations: what percentage of templates are current, major risks found, folders with the most problems, mislabeled files discovered]
- [Recommendations for immediate action before KB generation begins]
```

---

## Optional: Formatted Spreadsheet Export

The markdown output is the primary format — it's what the builder reads during KB generation. But for client presentations or consultant review, a formatted `.xlsx` version can be useful.

To convert the markdown audit to a spreadsheet, ask the builder to generate a CSV-ready version, then import it into Excel or Google Sheets and apply the following formatting:

**Columns:**
| A | B | C | D | E |
|---|---|---|---|---|
| Folder | File | KUAD | Reasoning | Notes |

**KUAD color coding (apply to entire row based on column C):**

| Tag | Row fill color | Text color |
|---|---|---|
| Keep | Green (#d9ead3) | Black |
| Update | Yellow (#fff2cc) | Black |
| Archive | Gray (#d9d9d9) | Dark gray |
| Delete | Red (#f4cccc) | Dark gray |

**Additional formatting:**
- Freeze the header row
- Auto-fit column widths (Reasoning and Notes columns will be widest)
- Add a filter to the header row so the audit can be filtered by KUAD tag or folder
- Include a separate "Summary" sheet with the tag counts and Key Findings

The spreadsheet is a presentation artifact — the markdown version remains the source of truth for the builder pipeline.

---

## Quality Checks

Before delivering the output:

- Every file in the storage inventory's key folders has been tagged
- No file is tagged without reasoning
- Stakeholder input from transcripts is reflected in tags where relevant
- Duplicate files are identified and only one version is tagged Keep
- Mislabeled files are flagged with correct descriptions
- Summary counts match the detailed tables
