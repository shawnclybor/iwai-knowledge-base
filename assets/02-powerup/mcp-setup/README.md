# MCP Setup

The Supabase MCP connector is bundled in the plugin (`.mcp.json`) and auto-starts on install. This folder has the detailed setup and troubleshooting docs.

## Connector in the Plugin

| Connector | Purpose | Used By |
|-----------|---------|---------|
| **Supabase MCP** | Apply migrations, query tables, run RPC functions | `/setup-rag`, `/calibrate`, pipeline scripts |

Supabase uses remote HTTP with OAuth (no access token needed). See `mcp-connector-setup.md` for details.

> **Note:** Document conversion (Stage 2) is handled by `convert.py` using lightweight Python libraries — no MCP connector needed.

## Files

- `mcp-connector-setup.md` — Setup details, verification steps, and troubleshooting for the Supabase connector
