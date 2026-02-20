# Recurring Questions Compilation

This document defines how to extract and compile recurring internal questions from processed discovery materials. The output is a categorized list of questions that the client's team asks repeatedly, which becomes a key input for gap analysis and KB file planning.

---

## When to Use

Use this template after processing at least one stakeholder interview transcript. The recurring questions list is an intermediate deliverable — it feeds directly into the gap analysis step.

---

## Required Inputs

- **Processed interview transcripts** — At minimum, one transcript. More transcripts produce more complete question coverage.
- **Storage/file inventory** (optional but recommended) — Helps confirm whether mentioned questions have any existing documentation.

---

## File Naming Convention

```
[client-short-name]-recurring-questions-[YYYY-MM-DD].md
```

**Example:** `acme-recurring-questions-2024-06-15.md`

---

## How to Extract Questions

Read through each transcript and identify:

1. **Explicit questions** — Questions that stakeholders say they or their colleagues ask regularly. Look for phrases like "people always ask," "I get asked this every week," "the most common question is."
2. **Implicit questions** — Pain points or workarounds that imply a missing answer. If a stakeholder describes searching for something, waiting for a specific person to respond, or learning something "the hard way," there's an underlying question.
3. **Frequency indicators** — Note how often the question comes up. Stakeholders often give cues: "daily," "every week," "constantly," "almost every new client."
4. **Who asks** — Note which roles or seniority levels ask each type of question. This informs who the KB needs to serve first.

---

## Output Format

Produce a single markdown file:

```
# [Client Name] — Top Recurring Internal Questions

*Compiled from stakeholder interviews with [names and roles]. These represent the questions asked most frequently via [channels mentioned] to [key people mentioned].*

---

## [Category Name]

1. **[Question as typically phrased]** — Asked by [who — role or "all consultants"], [frequency — e.g., "weekly," "multiple times per week," "constantly"]. [1-2 sentences of context: why the answer is hard to find, why it varies, or what goes wrong without it.]

2. **[Next question]** — Asked by [who], [frequency]. [Context.]

## [Next Category]

...

---

## Sources

- [List processed transcript files used to compile this list]
```

### Categorization

Group questions into categories that reflect the client's actual pain points, not a generic taxonomy. Derive category names from what the transcripts reveal. If the client's biggest pain point is template management, that might warrant two categories (finding templates vs. verifying templates) rather than one.

### Quantity

Aim for 15–25 questions total. If you find more, prioritize by frequency and impact. If you find fewer than 10, flag that additional interviews may be needed: `[CONTENT GAP — fewer than 10 recurring questions identified; additional stakeholder interviews recommended]`.

---

## Phrasing

Write each question the way the team would actually ask it, not in formal language. These should sound like real Slack messages or hallway questions:

- Good: "Which employee handbook template should I use for [client type + state]?"
- Bad: "What is the appropriate handbook template selection methodology?"

When a question varies by context (state, industry, client type), use bracketed variables to show the pattern.

---

## Quality Checks

Before delivering the output:

- Every question can be traced to a specific statement in a transcript
- Categories reflect the client's actual pain points, not generic topics
- Frequency and "who asks" are noted for each question
- No fabricated questions — if something seems likely but wasn't mentioned in the transcripts, do not include it
- Questions are phrased naturally, the way the team would actually ask them
