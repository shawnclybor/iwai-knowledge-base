---
description: "Review query logs, detect stale content, and maintain the knowledge base"
---

# Lesson 3 Maintain

Analyze search usage, detect stale content, and maintain the knowledge base.

## Before You Start

Read `assets/03-advanced/templates/maintenance-ops.md` for background on query log analysis and stale content detection.

## Step 1: Query Log Analysis

Run these queries via Supabase MCP to understand search usage:

```sql
-- Usage overview
SELECT count(*) as total_queries,
       round(avg(latency_ms)) as avg_latency_ms,
       min(created_at) as first_query,
       max(created_at) as last_query
FROM query_log;
```

```sql
-- Zero-result queries (knowledge gaps)
SELECT query_text, created_at
FROM query_log
WHERE result_count = 0
ORDER BY created_at DESC
LIMIT 10;
```

```sql
-- Low-score queries (poor retrieval)
SELECT query_text, top_score, search_mode, reranked
FROM query_log
WHERE top_score < 0.5
ORDER BY top_score ASC
LIMIT 10;
```

```sql
-- Search mode distribution
SELECT search_mode, reranked, count(*), round(avg(latency_ms)) as avg_ms
FROM query_log
GROUP BY search_mode, reranked;
```

Summarize findings for the student. Highlight:
- Any zero-result queries (potential gaps in the knowledge base)
- Low-score queries (might benefit from reranking or different chunking)
- Latency patterns (is reranking adding too much time?)

## Step 2: Stale Content Detection

Check if source files have changed since ingestion:

```bash
# Compute current hashes of source files
cd assets/02-powerup/source-files
for f in *; do
  echo "$(shasum -a 256 "$f" | cut -d' ' -f1)  $f"
done
```

Compare against the database:

```sql
SELECT file_name, file_hash, status, processed_at
FROM file_metadata
WHERE status = 'completed'
ORDER BY file_name;
```

Report any mismatches. If a file's hash has changed since ingestion, it's stale.

## Step 3: Re-ingestion (if needed)

If stale files are found, offer to re-ingest them using Lesson 2's pipeline:

```bash
cd assets/02-powerup/pipeline/scripts
python ingest.py --source-dir ../../source-files
python convert.py
python chunking.py
python embed.py
```

The pipeline's hash-based dedup will detect changed files automatically. Unchanged files are skipped.

## Step 4: Summary

Present a maintenance summary:
- Total queries logged
- Knowledge gaps identified (zero-result queries)
- Stale files detected (if any)
- Re-ingestion status (if performed)
- Recommendation: when to run this check again (weekly for active KBs)
