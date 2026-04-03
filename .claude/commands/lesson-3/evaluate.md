---
description: "Run the Lesson 3 evaluation harness and view results in Langfuse"
---

# Lesson 3 Evaluate

Run the evaluation harness to score retrieval quality with Ragas metrics and push traces to Langfuse.

## Before You Start

Read `assets/03-advanced/templates/evaluation-harness.md` for background on Langfuse, Ragas metrics, and how to interpret results.

## Pre-flight Checks

1. Verify `MCP_SERVER_READY=1` in `assets/03-advanced/.env`
2. Verify Langfuse credentials are set in `.env` (LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY, LANGFUSE_BASE_URL)
3. Verify Python dependencies are installed: `python -c "import langfuse, ragas, openai, supabase"`

If any check fails, run `/lesson-3:setup` first.

## Run Evaluation

Activate the virtual environment and run the harness:

```bash
cd assets/03-advanced && source .venv/bin/activate && cd evaluation && python evaluate.py
```

If the venv doesn't exist yet, create it first:

```bash
cd assets/03-advanced && python3 -m venv .venv && source .venv/bin/activate && pip install -r evaluation/requirements.txt
```

Walk the student through the output:
- Each query is processed sequentially (embed → search → generate → score)
- The summary table shows Ragas scores per query
- The Langfuse dashboard URL is printed at the end

## Review Results

After the script completes:

1. **Terminal summary** — explain each metric column:
   - **Faith** = Faithfulness (is the answer grounded in context?)
   - **Relev** = Answer Relevancy (does the answer address the question?)
   - **Prec** = Context Precision (are relevant chunks ranked higher?)
   - **Src** = Source hit (did the expected file appear in results?)

2. **Langfuse dashboard** — guide the student to:
   - Open the printed URL
   - Navigate to Traces
   - Click a trace to see spans (embedding, retrieval, generation, scoring)
   - Check the Scores tab for aggregate metrics

3. **Identify weak spots** — look for:
   - Queries with faithfulness < 0.8 (potential hallucination)
   - Queries with context precision < 0.7 (retrieval returning wrong chunks)
   - Source misses (expected file not in top results)

## Set Flag

Update `assets/03-advanced/.env`: set `EVALUATION_COMPLETE=1`.

Suggest next steps: "You can re-run evaluation after tuning search parameters or run `/lesson-3:maintain` to check the query log."
