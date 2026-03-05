# Sample Calibration Report

This is an example output from the `rag-reviewer` agent after a successful pipeline run.

---

## Pipeline Health Report

**Status:** PASS

### File Processing

| Metric | Value |
|--------|-------|
| Total files | 11 |
| Completed | 11 |
| Failed | 0 |

| File Type | Count |
|-----------|-------|
| md | 5 |
| csv | 2 |
| docx | 2 |
| pdf | 2 |

### Chunk Statistics

| Metric | Value |
|--------|-------|
| Total chunks | ~85-110 |
| Average tokens | ~350 |
| Min tokens | ~55 |
| Max tokens | ~595 |

### Chunking Strategies Used

| Strategy | Files |
|----------|-------|
| chunk_by_headings | 9 (md, docx, pdf) |
| chunk_csv_rows | 2 (csv) |

### Quality Checks

- [ ] No orphaned chunks (chunks without valid file_id): **PASS**
- [ ] No null embeddings: **PASS**
- [ ] All chunks have metadata: **PASS**
- [ ] No chunks below 50 tokens: **PASS**
- [ ] No chunks above 700 tokens: **PASS**
- [ ] Full-text search index active: **PASS**
- [ ] HNSW vector index active: **PASS**

### Search Readiness

- Full-text search test (`safety policy`): Returns results — **PASS**
- Vector similarity search: Index present — **PASS**
- Hybrid search RPC: Function exists — **PASS**

---

## Recommendations

None. Pipeline output is healthy and search-ready.

If this were a production deployment, consider:
1. Adding more source documents to improve coverage
2. Testing with real user queries to calibrate hybrid search weights
3. Setting up incremental ingestion for new documents (the pipeline already supports this via SHA256 dedup)
