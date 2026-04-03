# Evaluation Harness — Background Reading

Read this before running the evaluation step.

---

## What Is an Evaluation Harness?

An evaluation harness is a test suite for your RAG pipeline. Instead of manually asking questions and eyeballing the answers, you run a predefined set of queries through the full pipeline — embedding, retrieval, generation — and automatically score the results.

Think of it like unit tests for search quality. You write the test queries, define what "good" looks like (which source files should appear, what the answer should cover), and the harness runs them all, scores them, and shows you where the system is strong and where it's weak.

**What our harness does, step by step:**

1. Loads 15 test queries from `datasets/truepoint-queries.json`
2. For each query:
   - Embeds the query (OpenAI)
   - Searches the KB via `hybrid_search()` RPC (same path as the MCP server)
   - Generates an answer using GPT-4o-mini with the retrieved context
   - Scores the result using Ragas metrics (faithfulness, relevancy, precision)
   - Checks whether the expected source file appears in the results
   - Pushes the full trace (timing, inputs, outputs, scores) to Langfuse
3. Prints a summary table and identifies weak spots

The harness does NOT go through the MCP server — it calls the RPCs directly. This means you can run it independently, and the results measure the quality of your data and search functions, not the MCP wrapper.

**Important: SDK versions.** The evaluation harness is built for **Langfuse v4** and **Ragas v0.4**. Key API details:
- Langfuse v4 uses `start_observation()` instead of the older `trace()` API
- Ragas v0.4 returns scores via `result.scores` (a list of dicts), not via dict-style `result["metric"]`
- Ragas `context_precision` requires a `reference` column (renamed from `ground_truth` in earlier versions)
- The harness passes explicit LLM and embedding wrappers to Ragas to avoid auto-detection issues

The pinned versions in `requirements.txt` ensure you get a compatible combination.

## Setting Up Langfuse

Langfuse is a free, open-source observability platform for LLM applications. You need an account before running the evaluation.

**Setup steps:**

1. Go to [cloud.langfuse.com](https://cloud.langfuse.com) and create a free account
2. Create a new project (name it something like "truepoint-kb-eval")
3. Go to **Settings > API Keys** and create a new key pair
4. You'll get three values:
   - **Public Key** (`pk-lf-...`) — identifies your project
   - **Secret Key** (`sk-lf-...`) — authenticates writes
   - **Base URL** — `https://us.cloud.langfuse.com` (US region)
5. These go into your `assets/03-advanced/.env` file as:
   ```
   LANGFUSE_PUBLIC_KEY=pk-lf-...
   LANGFUSE_SECRET_KEY=sk-lf-...
   LANGFUSE_BASE_URL="https://us.cloud.langfuse.com"
   ```

After running the evaluation, go to your Langfuse project dashboard to see the traces, spans, and scores visually.

## Why Langfuse (and Not Just Terminal Output)?

The terminal output gives you a summary table — good for a quick check. Langfuse gives you:

- **Drill-down per query** — click any trace to see the exact chunks retrieved, the generated answer, and each metric score
- **Span timing** — see where latency comes from (embedding? retrieval? generation?)
- **Score trends over time** — run the harness again after making changes and compare
- **Shareable dashboards** — show a client that their KB is performing well

## Why Evaluate RAG?

Building a search pipeline is not enough — you need to know if it actually returns good results. Evaluation answers: "When a user asks a question, does the system retrieve the right content and generate an accurate answer?"

Without evaluation, you're flying blind. A search might return high similarity scores but miss the relevant document entirely.

## Langfuse Concepts

Think of Langfuse as "logs + metrics + traces" for AI pipelines.

**Key concepts:**

- **Trace** — a single end-to-end execution (one query through the full pipeline)
- **Span** — a step within a trace (embedding, retrieval, generation, scoring)
- **Score** — a numeric metric attached to a trace (faithfulness: 0.85)

Our evaluation harness creates one trace per test query, with spans showing timing and outputs for each step, and Ragas scores attached at the end.

**What you see in the dashboard:**
```
Trace: eval-query-1 "What are the FMLA eligibility requirements?"
├── Span: embedding        (12ms, model: text-embedding-3-small)
├── Span: retrieval        (45ms, 10 results, sources: fmla-policy-2023.md, ...)
├── Span: generation       (380ms, model: gpt-4o-mini)
├── Span: scoring          (Ragas metrics computed)
└── Scores:
    ├── faithfulness: 0.92
    ├── answer_relevancy: 0.88
    └── context_precision: 0.95
```

## Ragas Metrics

Ragas provides reference-free evaluation metrics for RAG systems. "Reference-free" means you don't need human-annotated golden answers for every query (though they help).

### Context Precision

**What it measures:** Are the retrieved chunks that are relevant ranked higher than the irrelevant ones?

**Scale:** 0-1 (1 = all relevant chunks at the top)

**Why it matters:** Even if the right chunk is retrieved, if it's buried at position 8 out of 10, the LLM might not use it effectively. Context precision catches this.

### Faithfulness

**What it measures:** Is the generated answer factually grounded in the retrieved context? Can every claim in the answer be traced back to a retrieved chunk?

**Scale:** 0-1 (1 = fully grounded, no hallucination)

**Why it matters:** This is your hallucination detector. A low faithfulness score means the LLM is making claims that aren't supported by the retrieved documents.

### Answer Relevancy

**What it measures:** Does the generated answer actually address the question? Is it on-topic and responsive?

**Scale:** 0-1 (1 = perfectly addresses the question)

**Why it matters:** The answer might be faithful to the context but not answer what was asked. This metric catches "technically correct but unhelpful" responses.

## The Evaluation Dataset

The test dataset (`datasets/truepoint-queries.json`) contains queries with:

- `question` — the test query
- `expected_sources` — which source files should appear in results (for source accuracy checking)
- `ground_truth` — optional reference answer (improves some metrics)

The `contexts` and `answer` fields are generated at evaluation time — they are not pre-populated.

## Interpreting Results

**Good scores (generally):**
- Faithfulness > 0.8 — answers are well-grounded
- Answer Relevancy > 0.7 — answers are on-topic
- Context Precision > 0.7 — relevant chunks are ranked well

**Red flags:**
- Faithfulness < 0.5 — significant hallucination, check chunk quality
- Context Precision < 0.5 — retrieval is returning wrong chunks, check embeddings or try reranking
- Source misses — expected files not appearing in results, check if they were ingested correctly
