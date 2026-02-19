# Knowledge Gap Compilation

This document defines how to identify and document knowledge gaps by cross-referencing recurring questions against available documentation. The output is a structured gap list that directly informs which KB files need to be created.

---

## When to Use

Use this template after you have:

- A compiled recurring questions list (see `recurring-questions.md`)
- A storage/file inventory showing what documentation currently exists
- Optionally, a document inventory with KUAD tags and/or sample client documents

---

## Required Inputs

- **Recurring questions list** — The compiled output from `recurring-questions.md`
- **Storage/file inventory** — The client's folder and file structure
- **Document inventory with KUAD tags** (if available) — Provides status information about existing documents
- **Sample client documents** (if available) — Helps assess whether existing docs actually answer the questions

---

## How to Identify Gaps

For each recurring question (or cluster of related questions), ask:

1. **Does documentation exist that answers this?** Search the file inventory for relevant documents.
2. **If yes, is it current and reliable?** Check KUAD tags, modification dates, and auditor notes. A document marked "Update" or "Archive" is a partial gap.
3. **If yes, is it findable?** A document that exists but is buried in the wrong folder, mislabeled, or unknown to the team is functionally a gap.
4. **If no, where does the answer currently live?** Usually in one person's head. Note who holds the knowledge — that's the follow-up source for filling the gap.

### Gap Types

Each gap falls into one of three types:

- **No documentation exists** — The answer is purely tribal knowledge. Highest priority.
- **Documentation exists but is outdated or incomplete** — Content exists but can't be trusted as-is. Needs update.
- **Documentation exists but is unfindable or scattered** — Content is technically there but the team can't access it practically. Needs consolidation and indexing.

---

## Output Format

Produce a single markdown file:

```
# [Client Name] — Knowledge Gap List

*Compiled from discovery interviews, content audit, and storage inventory review. Each gap represents a question asked regularly by staff that has no reliable documented answer.*

---

## How to Read This List

Each gap includes:

- **Question** — How the question is typically asked
- **Who asks** — Role(s) and frequency
- **Current workaround** — How it's handled today
- **Why it's a gap** — What's missing and what risk it creates
- **Recommended KB file** — Where the answer should live once the knowledge base is built

---

## Gap [N]: [Short Descriptive Title]

**Question:** "[Question as typically asked by staff]"
**Who asks:** [Role(s)], [frequency — e.g., daily, weekly, when covering clients]
**Current workaround:** [How it's handled today — e.g., ask a specific person, search and guess, skip it]
**Why it's a gap:** [What's missing, what goes wrong, what risk it creates]
**Recommended KB file:** `[suggested-filename.md]`

---

[Repeat for each gap identified. Number sequentially.]

---

## Summary

| Gap Category | # of Gaps | Impact Level |
|---|---|---|
| [Category name] | [count] | [HIGH / MEDIUM / LOW — with brief justification] |

**Total gaps identified:** [#]
**Gaps with no existing documentation:** [#]
**Gaps with outdated or incomplete documentation:** [#]

---

## Sources

- [List discovery files used to compile this gap list]
- [e.g., stakeholder-interview-transcript-YYYY-MM-DD.md]
- [e.g., storage-inventory.md]
- [e.g., document-inventory.xlsx]
```

---

## Impact Assessment

Assign impact levels based on:

- **HIGH** — Creates compliance risk, causes client-facing errors, or blocks daily work
- **MEDIUM** — Slows the team down, creates dependency on specific people, or extends onboarding time
- **LOW** — Inconvenient but has workable alternatives, or affects a small number of situations

---

## Connecting Gaps to KB Files

The "Recommended KB file" field is a suggestion, not a final assignment. During the source assessment step, the consultant and builder will finalize which KB files to create and which gaps each file addresses.

When suggesting KB file names:

- Use descriptive, lowercase, hyphenated names
- Group related gaps into the same recommended file when they share a topic
- Don't create a separate file per gap — consolidate where it makes sense

---

## Quality Checks

Before delivering the output:

- Every gap traces back to at least one recurring question
- The current workaround is documented for each gap (this reveals who holds the knowledge)
- Impact levels are justified, not arbitrary
- Recommended KB files are realistic — not too granular (one file per question) or too broad (one file for everything)
- The summary table accurately reflects the gap count and categories
- Gaps involving outdated documentation reference the specific outdated file(s) from the inventory
