# Template: Chunking Router

**Pipeline Stage:** 3 of 5
**Input:** Normalized markdown + document structure (from document conversion)
**Output:** List of chunks with metadata for each file

---

## What This Step Does

Analyzes each converted document and selects the best chunking strategy based on file type and structure. Different document types need different approaches — a well-structured Word doc chunks differently than a CSV or a flat PDF.

## Strategy Selection

| File Type | Primary Strategy | Fallback | Notes |
|-----------|-----------------|----------|-------|
| **pdf** | Document-structure (headings/sections) | Recursive with overlap | pdfplumber preserves text and tables |
| **docx** | Document-structure (heading levels) | Recursive with overlap | Word docs typically have clear H1/H2/H3 |
| **md** | Header-based splitting (`##` and `###`) | Recursive with overlap | Already structured |
| **csv** | Row-group chunking | Per-row with header prepend | Each chunk = N rows with column context |

## Common Parameters

- **Max chunk size:** ~600 tokens (tunable)
- **Overlap:** 10–15% between adjacent chunks
- **Minimum chunk size:** 50 tokens (merge small fragments with neighbors)

## Chunk Metadata

Capture this metadata for every chunk:

```json
{
  "section_heading": "Safety Equipment Requirements",
  "chunk_index": 3,
  "hierarchy_level": 2,
  "has_table": false
}
```

| Field | Description |
|-------|------------|
| `section_heading` | Nearest heading above the chunk |
| `chunk_index` | Position in document (0-indexed) |
| `hierarchy_level` | Heading depth: 1 = H1, 2 = H2, etc. |
| `has_table` | Whether the chunk contains tabular data |

## Strategy Details

### Document-Structure (for pdf, docx, md)

1. Parse the markdown for headings (`#`, `##`, `###`)
2. Split at heading boundaries
3. If a section exceeds max chunk size, recursively split at paragraph boundaries
4. Add overlap by including the last 1–2 sentences of the previous chunk at the start

### Row-Group (for csv)

1. Parse the CSV headers
2. Group rows into chunks of N rows (default: 10)
3. Prepend column headers to each chunk for context
4. Format as readable text, not raw CSV

### Recursive with Overlap (fallback)

Used when a document has no clear structure:

1. Split at paragraph boundaries (`\n\n`)
2. If paragraphs exceed max size, split at sentence boundaries
3. Maintain overlap between adjacent chunks

## Verification

After this step, check:
- [ ] Every file produced at least one chunk
- [ ] No chunk exceeds ~600 tokens
- [ ] No chunk is below 50 tokens (merged with neighbors)
- [ ] CSV chunks include column headers
- [ ] Chunk metadata is populated (section_heading, chunk_index at minimum)
- [ ] Total token count is reasonable for the source file sizes
