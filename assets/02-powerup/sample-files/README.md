# Sample Files

Expected outputs from the pipeline, for verification. Use these to confirm your pipeline is producing correct results.

## What's Here

| File | What It Shows |
|------|--------------|
| `sample-query-results.md` | Example output from `match_chunks` and `hybrid_search` with 3 test queries |
| `sample-calibration-report.md` | Example calibration output showing precision/recall at different threshold settings |

## How to Use

After running the full pipeline (ingest → chunk → embed → upsert):

1. Run the test queries in `sample-query-results.md` against your database
2. Compare your results to the expected output
3. If results differ significantly, check:
   - Were all source files ingested? (Check `file_metadata` for status = 'completed')
   - Are embeddings populated? (Check `chunks` for non-null embedding column)
   - Is the similarity threshold appropriate? (Default 0.78 may need tuning)

## Generating Your Own Samples

Use the `/calibrate` skill to generate fresh calibration reports against your actual data.
