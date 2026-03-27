# Lesson 3: Advanced — Deploy the Knowledge

Wire Claude Code to Supabase for live KB search, connect evaluation tooling via Langfuse, run tests, and iterate on retrieval quality.

## What You'll Build

A custom MCP server that gives Claude direct search access to the Lesson 2 knowledge base, an evaluation harness that measures retrieval quality, and a maintenance workflow for ongoing improvement.

## Prerequisites

- **Lesson 2 completed** — Supabase populated with embedded chunks, RPC functions exist
- **Node.js >= 18** — for the MCP server
- **Python 3.10+** — for the evaluation harness
- **API keys (3):** Supabase (from L2), OpenAI (from L2), Langfuse (free at [langfuse.com](https://langfuse.com/))

## Quick Start

```
/lesson-3:setup       # Environment, deps, migration, MCP server deploy
/lesson-3:evaluate    # Run evaluation harness, view results in Langfuse
/lesson-3:maintain    # Query log analysis, stale content detection
```

## The Build → Index → Deploy Arc

| Lesson | Verb | What It Produces |
|--------|------|-----------------|
| 1. Core | **Build** | Structured KB files from raw discovery materials |
| 2. Power-Up | **Index** | Embedded, searchable chunks in Supabase |
| 3. Advanced | **Deploy** | Live Claude search + quality metrics + maintenance loop |

Lesson 2 made the KB searchable via SQL. Lesson 3 makes it usable — Claude can search it directly, you can measure quality, and you know when content goes stale.

## Key Concepts

**MCP server (kb-search):** A custom TypeScript server that wraps the Supabase RPCs (`hybrid_search()`, `match_chunks()`) into tools Claude can call directly. It embeds the query via OpenAI, searches the KB, optionally reranks results with GPT-4o-mini, and logs every search to `query_log`. See `templates/search-and-rpc.md` for the full technical breakdown.

**RPC (Remote Procedure Call):** Functions stored in Supabase that you call by name instead of writing raw SQL. Lesson 2 created `hybrid_search()` and `match_chunks()`. The MCP server wraps these so Claude doesn't need to know SQL.

**Evaluation harness:** A test suite for your RAG pipeline. Runs 15 predefined queries through the full pipeline (embed → search → generate → score), measures quality with Ragas metrics, and pushes traces to Langfuse. See `templates/evaluation-harness.md`.

**Ragas metrics:** Faithfulness (is the answer grounded in context?), answer relevancy (does it address the question?), context precision (are relevant chunks ranked high?). All scored 0-1.

**Query logging:** Every MCP search is logged — query text, result count, top score, latency, search mode. This data drives the maintenance workflow: zero-result queries reveal knowledge gaps, low scores reveal retrieval problems.

## Lesson Flow (5 Parts)

### Part 1: Review the Repo
Understand what Lesson 2 produced (chunks, embeddings, RPCs) and what Lesson 3 adds (MCP server, evaluation, query logging, maintenance).

### Part 2: Set Up the Tooling
Connect Supabase MCP, run kb-auditor to validate L2 output, apply query_log migration, deploy the kb-search MCP server, set up Langfuse credentials.

### Part 3: Run Queries
First live search through the MCP server. Compare hybrid vs vector-only vs hybrid+rerank. Inspect query_log. Understand when to use each mode.

### Part 4: Evaluation Harness
Run `evaluate.py` against 15 test queries. Review Ragas scores in Langfuse. Identify weak spots — which queries scored low, which sources were missed.

### Part 5: The Iteration Loop
Find a problem → diagnose → fix → re-test. Zero-result queries mean add content. Low faithfulness means check chunk quality. Low precision means try reranking or adjust weights. See `templates/maintenance-ops.md` for the full playbook.

## Folder Structure

```
03-advanced/
├── README.md                    ← You are here
├── recordings/                  ← Session transcript (when available)
├── slides/                      ← Session slide deck (when available)
│
├── builder-tools/
│   └── instructions.md          ← 7-step workflow
│
├── mcp-server/                  ← Custom TypeScript MCP server
│   └── src/
│       ├── index.ts             ← Entry point
│       ├── tools/
│       │   ├── search-kb.ts     ← embed → search → rerank → log
│       │   └── list-sources.ts  ← query file_metadata
│       └── lib/
│           └── supabase.ts      ← Client initialization
│
├── evaluation/                  ← Python evaluation harness
│   ├── evaluate.py
│   ├── requirements.txt
│   └── datasets/
│       └── truepoint-queries.json  ← 15 test queries
│
├── migrations/
│   └── 004_create_query_log.sql
│
├── templates/                   ← Background reading (read before each part)
│   ├── search-and-rpc.md        ← Part 3: How search, RPC, and hybrid search work
│   ├── mcp-server-build.md      ← Part 2: What MCP servers are, how kb-search works
│   ├── evaluation-harness.md    ← Part 4: What Ragas measures, how Langfuse works
│   └── maintenance-ops.md       ← Part 5: Query logs, stale content, the iteration loop
│
└── sample-files/
    ├── sample-search-results.md
    └── sample-evaluation-report.md
```

## Commands

| Command | What It Does |
|---------|-------------|
| `/lesson-3:setup` | Prerequisites, env vars, deps, migration, MCP server deploy |
| `/lesson-3:evaluate` | Run evaluation harness, view results in Langfuse |
| `/lesson-3:maintain` | Query log analysis, stale content detection |

## Tech Stack

| Component | Tool | Purpose |
|-----------|------|---------|
| MCP Server | TypeScript + `@modelcontextprotocol/sdk` | Wraps Supabase RPCs for Claude |
| Search | `hybrid_search()` + `match_chunks()` | Vector + keyword hybrid retrieval |
| Reranking | GPT-4o-mini | Optional LLM-based relevance re-scoring |
| Evaluation | Langfuse + Ragas | Retrieval quality metrics + observability |
| Logging | Supabase `query_log` table | Search analytics for maintenance |

## Operational Costs (Incremental Over L2)

| Service | Cost | Notes |
|---------|------|-------|
| Langfuse | Free tier | Generous limits for evaluation and tracing |
| OpenAI (reranking) | ~$0.01/query | Only when reranking is enabled |
| **Total incremental** | **~$0/month** | Langfuse free tier + minimal reranking usage |

## What This Lesson Produces

A running MCP server giving Claude live KB search, an evaluation baseline in Langfuse showing retrieval quality across 15 test queries, a populated `query_log` table for ongoing monitoring, and a maintenance workflow for detecting and fixing content gaps, stale documents, and retrieval problems. The knowledge base is now usable, measurable, and maintainable.
