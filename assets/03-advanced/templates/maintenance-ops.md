# Maintenance Operations — Background Reading

Read this before Step 7 (Maintenance Workflow) in the instructions.

---

## Why Maintenance Matters

A knowledge base that isn't maintained degrades over time. Source documents change, new content is added, and usage patterns reveal gaps. The query log and file metadata give you the data to catch these issues early.

## Query Log Analysis

The `query_log` table records every search through the MCP server. Useful queries:

### Usage overview

```sql
SELECT count(*) as total_queries,
       avg(latency_ms) as avg_latency_ms,
       min(created_at) as first_query,
       max(created_at) as last_query
FROM query_log;
```

### Zero-result queries (knowledge gaps)

```sql
SELECT query_text, created_at
FROM query_log
WHERE result_count = 0
ORDER BY created_at DESC
LIMIT 20;
```

These are questions the knowledge base can't answer. Each one is either a gap to fill (add new content) or a search tuning opportunity (adjust weights or thresholds).

### Low-score queries (poor retrieval)

```sql
SELECT query_text, top_score, search_mode, reranked
FROM query_log
WHERE top_score < 0.5
ORDER BY top_score ASC
LIMIT 20;
```

Low top scores suggest the query doesn't match available content well. Consider: Is the content present but chunked poorly? Is the query too vague? Would reranking help?

### Search mode distribution

```sql
SELECT search_mode, reranked, count(*), avg(latency_ms)
FROM query_log
GROUP BY search_mode, reranked;
```

Shows how the search is being used. If reranking is rarely used, it might not be needed. If latency is high with reranking, consider reducing the number of results to rerank.

## Stale Content Detection

When source documents change after ingestion, the knowledge base becomes stale. The `file_metadata` table stores SHA256 hashes of every ingested file.

**Detection approach:**
1. Scan the source files directory
2. Compute current SHA256 hashes
3. Compare against `file_metadata.file_hash`
4. Any mismatch = stale content that needs re-ingestion

```sql
-- Check current file statuses
SELECT file_name, status, file_hash, processed_at
FROM file_metadata
ORDER BY file_name;
```

The `/lesson-3:maintain` command automates this comparison.

## Re-ingestion

When stale files are detected, re-ingest them using Lesson 2's pipeline:

1. The pipeline's hash-based dedup will detect the changed file
2. Old chunks for that file are deleted (CASCADE from file_metadata)
3. New chunks are generated and embedded
4. The file's status returns to `completed` with updated hash

This is safe — unchanged files are skipped automatically.

## The Iteration Loop: Finding and Fixing Problems

The query log and evaluation harness tell you *what's wrong*. This section tells you *what to do about it*.

### Problem: Zero-Result Queries (Knowledge Gaps)

**What it looks like:** `result_count = 0` in the query log. The user asked a question and got nothing back.

**Diagnosis:** The content doesn't exist in the KB, or exists but wasn't chunked/embedded properly.

**Fix options:**
1. **Add new content** — Write a new KB file covering the topic, then re-run the L2 pipeline to ingest it
2. **Check for chunking issues** — If the content exists but wasn't found, the chunk may be too large (burying the relevant text) or too small (losing context). Run the kb-auditor to check chunk sizes
3. **Lower the similarity threshold** — If the content is conceptually related but uses different terminology, the vector search threshold may be too strict

### Problem: Low Faithfulness Scores (Hallucination)

**What it looks like:** Faithfulness < 0.8 in the evaluation harness. The generated answer makes claims not supported by the retrieved chunks.

**Diagnosis:** Either the right chunks weren't retrieved (retrieval problem) or the LLM is ignoring the context (generation problem).

**Fix options:**
1. **Check what was retrieved** — Look at the Langfuse trace for that query. Are the right chunks in the context? If not, it's a retrieval problem (see below)
2. **Improve chunk quality** — If the right content is retrieved but buried in a large chunk with irrelevant text, the LLM may latch onto the wrong part. Re-chunk the source file with smaller target sizes
3. **Strengthen the system prompt** — Add instructions like "Only answer based on the provided context. If the context doesn't contain the answer, say so"

### Problem: Low Context Precision (Wrong Chunks Ranked High)

**What it looks like:** Context Precision < 0.7 in the evaluation harness. Relevant chunks exist but are ranked below irrelevant ones.

**Diagnosis:** The search is returning the right chunks but not prioritizing them correctly.

**Fix options:**
1. **Enable reranking** — If you're not using it, try `rerank=true`. The LLM-based reranker is much better at distinguishing "similar" from "relevant"
2. **Adjust hybrid weights** — If keyword-heavy queries are performing poorly, increase the text weight (e.g., 0.5/0.5 instead of 0.7/0.3). If semantic queries are suffering, increase vector weight
3. **Improve chunk metadata** — Adding descriptive headers or section titles to chunks helps both vector and keyword search

### Problem: Source Misses (Expected File Not in Results)

**What it looks like:** The evaluation harness reports a source miss — the expected file didn't appear in the top results.

**Diagnosis:** The file might not be ingested, might have failed processing, or its chunks might not match the query well.

**Fix options:**
1. **Check file_metadata** — Is the file's status `completed`? If `failed`, re-run the L2 pipeline
2. **Check chunk count** — If the file produced very few chunks, it may have been poorly parsed. Check the converted output
3. **Test with vector-only search** — If the file appears in vector search but not hybrid, the full-text index may not have the right terms. Check that the tsvector was generated correctly

### Problem: High Latency

**What it looks like:** `latency_ms > 500` for non-reranked searches, or `> 3000` for reranked searches.

**Diagnosis:** Usually caused by too many results being processed or network latency to Supabase.

**Fix options:**
1. **Reduce match_count** — Search for 5 results instead of 10. Fewer chunks = less processing time
2. **Check Supabase region** — If your Supabase project is in a distant region, search latency will be higher
3. **Use vector-only for speed-critical paths** — Skip the full-text merge when speed matters more than keyword matching

### The Fix Cycle

After making a fix, verify it worked:

1. **Re-run the evaluation harness** — Compare the new scores against the previous run
2. **Check Langfuse** — The new traces appear alongside the old ones. Are the weak queries stronger now?
3. **Review the query log** — After the fix is in production, do the same queries still produce low scores or zero results?

This is not a one-time process. As source documents change, as users ask new types of questions, and as the KB grows, the cycle continues: **monitor → identify → fix → verify**.

## Maintenance Cadence

For a production knowledge base:

| Check | Frequency | Action |
|-------|-----------|--------|
| Query log review | Weekly | Identify gaps and tuning opportunities |
| Stale content scan | On source file updates | Re-ingest changed files |
| Full evaluation | Monthly | Run the evaluation harness, compare scores to baseline |
| Chunk quality audit | Quarterly | Run the kb-auditor agent for a comprehensive review |
