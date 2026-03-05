# Template: Document Conversion

**Pipeline Stage:** 2 of 5
**Input:** List of files to process (from file intake)
**Output:** Normalized markdown for each file, document structure metadata

---

## What This Step Does

Converts each source file to normalized markdown using lightweight Python libraries. The script handles different file formats — extracting text, preserving heading hierarchy, maintaining table structure, and identifying page boundaries.

## How to Run

```bash
python convert.py --input ./output/registered.json --output-dir ./output
```

## What It Does Per File Type

| Type | Library | Behavior |
|------|---------|----------|
| **md** | stdlib | Passes through unchanged. Extracts heading structure from `#` markers. |
| **docx** | `python-docx` | Extracts heading hierarchy (H1/H2/H3/H4), paragraphs, lists, and tables. Maps Word styles to markdown. |
| **pdf** | `pdfplumber` | Extracts text per page with `<!-- Page N -->` markers. Extracts tables. Detects section headings heuristically. |
| **csv** | stdlib `csv` | Converts to markdown table with header row and separator. Extracts column names and row count. |

## Output Format

For each file, the script produces a JSON entry in `output/converted.json`:

```json
{
  "file_metadata_id": "...",
  "file_name": "example.docx",
  "file_type": "docx",
  "markdown": "# Heading\n\nParagraph text...",
  "structure": {
    "headings": [{"level": 1, "text": "Heading"}]
  }
}
```

PDF files include `page_count` in structure. CSV files include `row_count` and `columns`.

## Error Handling

If conversion fails on a file:

1. The error is logged and the file is skipped
2. The pipeline continues to the next file
3. A summary of failures is printed at the end

## Verification

After this step, check:
- [ ] Every file has a markdown conversion (or a logged failure)
- [ ] Tables are preserved as markdown tables
- [ ] Heading hierarchy is intact (check a docx and pdf specifically)
- [ ] No binary garbage in the markdown output
