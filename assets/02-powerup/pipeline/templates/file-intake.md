# Template: File Intake

**Pipeline Stage:** 1 of 5
**Input:** Source folder path
**Output:** `file_metadata` rows in Supabase, list of files to process

---

## What This Step Does

Scans the source folder for supported file types, computes a SHA256 hash for each file, checks for duplicates in the database, and inserts a tracking row for each new or changed file.

## Supported File Types

- `.md` — Markdown
- `.docx` — Microsoft Word
- `.pdf` — PDF documents
- `.csv` — Comma-separated values

## Process

### 1. Scan Source Folder

Walk the source folder and collect all files with supported extensions. For each file, record:

- `file_name` — the filename (e.g., `construction-safety-policy.md`)
- `file_path` — full path to the file
- `file_type` — extension without dot (e.g., `md`)
- `file_size` — size in bytes

### 2. Compute File Hash

For each file, compute a SHA256 hash of the file contents. This is used for dedup and change detection.

```python
import hashlib

def compute_hash(file_path):
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()
```

### 3. Dedup Check

Query `file_metadata` for each hash:

- **Hash exists + status = 'completed'** → Skip. File hasn't changed.
- **Hash exists + status = 'failed'** → Retry. Delete old chunks and reprocess.
- **Hash not found** → New file. Insert a new row.

### 4. Insert Metadata

For new files, insert a row into `file_metadata` with `status = 'processing'`:

```sql
INSERT INTO file_metadata (file_name, file_path, file_type, file_size, file_hash, status)
VALUES ('construction-safety-policy.md', '/path/to/file', 'md', 4523, 'abc123...', 'processing');
```

### 5. Output

Return a list of files that need processing (new or retry). Each entry should include the `file_metadata.id` for downstream steps.

## Verification

After this step, check:
- [ ] All source files are accounted for in `file_metadata`
- [ ] No duplicate hashes
- [ ] New files have `status = 'processing'`
- [ ] Previously completed files were skipped
