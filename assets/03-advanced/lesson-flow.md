# Lesson 3: Advanced — Student Journey

```
┌─────────────────────────────────────────────────────────────────┐
│                    LESSON 3: GO LIVE                             │
│                                                                 │
│  Student opens repo in Claude Code                              │
│  Says "run lesson 3"                                            │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 1-3: SETUP                              /lesson-3:setup   │
│  ├── Check prerequisites (Node.js >= 18, Python 3.10+)          │
│  ├── Verify L2 completion (chunks in Supabase)                  │
│  ├── Set environment variables (Supabase, OpenAI, Langfuse)     │
│  ├── Install dependencies (npm + pip)                           │
│  ├── Apply migration 004 (query_log table)                      │
│  ├── Configure .mcp.json (merge kb-search server)               │
│  └── Restart Claude Code → verify MCP tools available           │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 4: BUILD + DEPLOY MCP SERVER                              │
│                                                                 │
│  ┌──────────────────────────────────────────────────────┐       │
│  │                  kb-search MCP Server                 │       │
│  │                                                       │       │
│  │  search_kb                    list_sources            │       │
│  │  ┌─────────────────────┐     ┌──────────────────┐    │       │
│  │  │ 1. Validate query   │     │ Query             │    │       │
│  │  │ 2. Embed (OpenAI)   │     │ file_metadata     │    │       │
│  │  │ 3. hybrid_search()  │     │ table             │    │       │
│  │  │    or match_chunks() │     └──────────────────┘    │       │
│  │  │ 4. Rerank (optional)│                              │       │
│  │  │ 5. Log to query_log │                              │       │
│  │  │ 6. Return results   │                              │       │
│  │  └─────────────────────┘                              │       │
│  └──────────────────────────────────────────────────────┘       │
│                                                                 │
│  Read: templates/mcp-server-build.md                            │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 5: TEST SEARCH + RERANKING                                │
│  ├── Run 5 queries in hybrid mode                               │
│  ├── Run same 5 queries in vector-only mode                     │
│  ├── Run same 5 queries with reranking enabled                  │
│  └── Compare results side-by-side                               │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 6: RUN EVALUATION                     /lesson-3:evaluate  │
│                                                                 │
│  evaluate.py                                                    │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐    │
│  │ Load dataset   │─▶│ For each query │─▶│ Push traces to │    │
│  │ (15-20 queries)│  │  embed → search │  │ Langfuse with  │    │
│  │                │  │  generate answer│  │ Ragas scores   │    │
│  │                │  │  score w/ Ragas │  │                │    │
│  └────────────────┘  └────────────────┘  └────────────────┘    │
│                                                                 │
│  Metrics: Context Precision, Faithfulness, Answer Relevancy     │
│  Read: templates/evaluation-harness.md                          │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 7: MAINTENANCE                       /lesson-3:maintain   │
│  ├── Query query_log for insights                               │
│  │    (zero-result queries, latency trends, usage patterns)     │
│  ├── Check file hashes against file_metadata for stale content  │
│  └── Optional: re-ingest changed files via L2 pipeline          │
│                                                                 │
│  Read: templates/maintenance-ops.md                             │
└─────────────────────────────────────────────────────────────────┘
```

## Architecture

```
Claude Code                      MCP Server (stdio)
┌────────────────┐               ┌──────────────────────┐
│ /lesson-3:     │               │ kb-search            │
│   setup        │               │                      │
│   evaluate     │───MCP tools──▶│ search_kb            │
│   maintain     │               │ list_sources         │
│                │◀──results─────│                      │
│ kb-auditor     │               └───────┬──────────────┘
│   agent        │                       │
└────────────────┘                       │
                                         ▼
  OpenAI API                    Supabase (pgvector)
┌────────────────┐              ┌──────────────────────────────┐
│ text-embedding │◀─embed──────│ file_metadata                │
│ -3-small       │              │ chunks (vector 1536)         │
│                │              │ query_log                    │
│ gpt-4o-mini   │◀─rerank─────│                              │
│ (optional)     │              │ hybrid_search() RPC          │
└────────────────┘              │ match_chunks() RPC           │
                                └──────────────────────────────┘

  Langfuse (cloud)
┌────────────────┐
│ Traces + Scores│◀─evaluate.py
│ Ragas metrics  │
│ Dashboard      │
└────────────────┘
```
