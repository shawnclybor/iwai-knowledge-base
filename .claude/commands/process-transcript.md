---
description: "Process a raw lesson transcript into structured lesson notes for a CLAUDE.md file"
---

# Process Transcript

Processes a raw recording transcript into structured, searchable lesson notes.

## Usage

```
/process-transcript <path-to-transcript>
```

Example: `/process-transcript assets/03-advanced/recordings/transcript.md`

## What This Does

1. Reads the raw transcript at the given path
2. Delegates processing to the `transcript-processor` agent (see `.claude/agents/transcript-processor.md` for processing rules)
3. Writes the output as a CLAUDE.md file in the lesson directory

## Steps

### Step 1: Validate Input

Check that the transcript file exists at the provided path. If no path is provided, check all lesson directories for unprocessed transcripts:

```
assets/*/recordings/transcript.md
```

A transcript is "unprocessed" if the parent lesson directory has no CLAUDE.md, or if the existing CLAUDE.md does not contain a "Lesson Notes" section.

### Step 2: Determine Output Location

The output goes to the CLAUDE.md in the lesson directory containing the transcript:
- `assets/01-core/recordings/transcript.md` → `assets/01-core/CLAUDE.md`
- `assets/02-powerup/recordings/transcript.md` → `assets/02-powerup/CLAUDE.md`
- `assets/03-advanced/recordings/transcript.md` → `assets/03-advanced/CLAUDE.md`

### Step 3: Process

Use the `transcript-processor` agent to process the transcript. The agent handles cleanup, structuring, and organization.

### Step 4: Write Output

- **If no CLAUDE.md exists:** Write the lesson notes as the new CLAUDE.md
- **If a CLAUDE.md already exists:** Append the lesson notes to the end, preceded by a separator:

```markdown
---

# Lesson [N]: [Title] -- Lesson Notes

The following is processed reference material from the live lesson recording.

[processed content]
```

### Step 5: Confirm

Report what was processed and where the output was written.
