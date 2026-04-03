# MCP Server Build — Background Reading

Read this before Step 4 (Build + Deploy MCP Server) in the instructions.

---

## What Is an MCP Server?

MCP (Model Context Protocol) is a standard for how AI tools connect to external data sources and services. Instead of building custom integrations, you build an MCP server that exposes **tools** — and any MCP-compatible client (Claude Code, Cowork, etc.) can use them.

An MCP server is a process that:
1. **Listens** for JSON-RPC requests over a transport (stdio, HTTP, etc.)
2. **Registers tools** — each tool has a name, description, and input schema
3. **Handles tool calls** — receives arguments, does work, returns results

Our MCP server uses **stdio transport** — Claude Code spawns it as a child process and communicates via stdin/stdout. This is the simplest transport: no networking, no ports, no CORS.

## The kb-search Server

Our server exposes two tools:

### `search_kb`

The main search tool. When Claude needs to answer a question from the knowledge base, it calls this tool.

**Flow:**
```
User question → Claude → search_kb tool call
                              ↓
                         1. Embed query (OpenAI text-embedding-3-small)
                              ↓
                         2. Call Supabase RPC
                            hybrid_search() or match_chunks()
                              ↓
                         3. Optional: rerank with GPT-4o-mini
                              ↓
                         4. Log to query_log (async)
                              ↓
                         5. Return formatted results → Claude → Answer
```

**Search modes:**
- `hybrid` (default): Combines vector similarity (semantic meaning) with full-text search (keyword matching). Best for most queries.
- `vector`: Pure vector similarity search. Good for exploratory or conceptual queries where exact terms matter less.

### `list_sources`

Returns a table of all files in the knowledge base with their status and chunk counts. Useful for Claude to understand what content is available.

## Re-ranking: Why Embeddings Aren't Enough

Embedding-based search measures **similarity** — how close two pieces of text are in meaning. But similarity is not the same as **relevance**. A chunk might be similar to your query (same topic) without actually answering it.

Re-ranking solves this with a second pass: after the initial search returns candidates, an LLM reads each result in context of the original query and scores it for actual relevance. This is a **reasoning** task, not a similarity task — that's why it needs an LLM (GPT-4o-mini) instead of an embedding model.

**Tradeoffs:**
- Re-ranking improves precision (better top results) at the cost of latency and API calls
- Each result requires one LLM call, so re-ranking 10 results = 10 API calls
- Default: disabled. Enable with `rerank: true` when precision matters more than speed

## How Claude Code Discovers the Server

The `.mcp.json` file at the repo root tells Claude Code about available MCP servers:

First compile the server: `cd assets/03-advanced/mcp-server && npx tsc`

```json
{
  "mcpServers": {
    "kb-search": {
      "command": "node",
      "args": ["/absolute/path/to/assets/03-advanced/mcp-server/dist/index.js"]
    }
  }
}
```

**Important:** Use an absolute path in `args` — do NOT use a relative path with `cwd`. The `cwd` field can cause tools to silently fail to register even though the server connects and responds to JSON-RPC. This matches the official MCP docs pattern. Also ensure no trailing blank lines in the `env` block.

Using compiled JS (`dist/index.js`) instead of `npx tsx` avoids startup noise on stderr that can interfere with the MCP stdio handshake.

Claude Code reads `.mcp.json` on startup, spawns the server process, and makes its tools available. After modifying `.mcp.json`, you must reload VS Code (Developer: Reload Window) to pick up changes.
