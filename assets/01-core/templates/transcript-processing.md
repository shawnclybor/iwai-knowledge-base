# Transcript Processing

Use this template to extract structured data from raw interview or meeting transcripts. The goal is to turn conversational audio transcripts into a scannable reference that the builder project can work from efficiently.

---

## When to Use

Use this template when you have a raw interview or meeting transcript (from Otter.ai, manual transcription, or similar). Process each transcript before using it as input for recurring questions, gap analysis, or KB file generation.

---

## Required Inputs

- **Raw transcript file** — Audio transcription in any text format (.txt, .md, .docx). Must include speaker identification.

---

## File Naming Convention

Name processed transcript files using this format:

```
[client-short-name]-transcript-[type]-[YYYY-MM-DD].md
```

**Examples:**
- `acme-transcript-discovery-2024-06-15.md`
- `acme-transcript-followup-2024-07-02.md`
- `acme-transcript-review-2024-08-10.md`

**Types:**
- `discovery` — Initial stakeholder interview
- `followup` — Follow-up session on specific topics
- `review` — Review of draft deliverables or audit findings

Keep the raw transcript file alongside the processed version. Name it:
```
[client-short-name]-transcript-[type]-[YYYY-MM-DD]-raw.[ext]
```

---

## How to Process

Read through the full transcript and extract data into the sections defined in the output format below. Guidance for each section:

- **Pain Points** — Extract each distinct pain point mentioned. Include who raised it and a supporting quote if one captures the point well.
- **Current Workflows** — Extract descriptions of how things work today — processes, tools, habits, workarounds. Note where workflows break down.
- **Specific Examples & Anecdotes** — Capture concrete stories — wrong template used, client lost, time wasted, mistake caught. These ground the pain points in real incidents.
- **Key Quotes** — Pull out quotes that are especially clear, quotable, or useful for understanding priorities. These are useful when writing KB files and citing stakeholder intent.
- **Stated Priorities** — What did participants say they want most? Capture "magic wand" answers and any explicit priorities.
- **Gaps Surfaced** — Questions or topics raised that have no documented answer. Feed these into the gap list.
- **Open Questions / Follow-ups** — Anything that needs clarification, a second conversation, or additional information before proceeding.

---

## Output Format

Produce a single markdown file using the naming convention above:

```
# [Client Name] — [Session Type] Transcript — [YYYY-MM-DD]

*Processed from raw transcript. See raw file for full conversation.*

---

## Metadata

| Field | Value |
|---|---|
| Client | [Client name] |
| Date | [YYYY-MM-DD] |
| Session type | [Discovery / Follow-up / Review] |
| Duration | [Length of recording] |
| Participants | [Name — Role, Name — Role, ...] |
| Transcript source | [Otter.ai / manual / other] |
| Raw file | [filename with extension] |

---

## Participants

| Name | Role | Context |
|---|---|---|
| [Name] | [Title / role at client org] | [Brief note: decision-maker, subject-matter expert, day-to-day user, etc.] |

---

## Pain Points Identified

1. **[Short label]** — [Description of the pain point. What's broken, what goes wrong, who's affected.]
   - Raised by: [Name]
   - Quote: "[Direct quote if it captures the point well]"

---

## Current Workflows Described

1. **[Workflow name / short label]** — [What they described. Steps, tools, who's involved, where it breaks down.]
   - Described by: [Name]

---

## Specific Examples & Anecdotes

1. **[Short label]** — [What happened, who was involved, what the consequence was.]
   - Mentioned by: [Name]

---

## Tools & Systems Mentioned

| Tool / System | What it's used for | Notes |
|---|---|---|
| [e.g., Google Drive] | [e.g., File storage] | [e.g., disorganized, 400+ files] |

---

## Key Quotes

> "[Quote]"
> — [Name], [context or topic]

---

## Stated Priorities

| Participant | Top priority | In their words |
|---|---|---|
| [Name] | [Short summary] | "[Quote or paraphrase]" |

---

## Gaps Surfaced

1. **[Topic]** — [What's missing. Who needs it. Why it matters.]

---

## Open Questions / Follow-ups

- [ ] [Question or action item]
- [ ] [Question or action item]
```

---

## Quality Checks

Before delivering the output:

- Every pain point and gap traces to a specific statement in the transcript
- Speaker attribution is accurate — the right person is credited for each point
- Key quotes are verbatim, not paraphrased
- No information is fabricated — if something is ambiguous in the transcript, note the ambiguity rather than guessing
- Open questions capture anything that needs follow-up before proceeding
