# MCP Connector Setup — RAG Pipeline

This document covers the Supabase MCP connection required for the RAG pipeline.

The connector is bundled in the plugin (`.mcp.json`) and auto-starts on install. This doc is for manual setup, troubleshooting, or understanding how it works.

> **Note:** Document conversion (Stage 2) is handled by `convert.py` using lightweight Python libraries (`python-docx`, `pdfplumber`) — no MCP connector needed.

---

## 1. Supabase MCP

### What It Does

Supabase MCP gives Claude direct access to your Supabase project's database. The pipeline uses it to:

- Apply migration SQL (create tables, indexes, RPC functions)
- Insert file metadata and chunks during ingestion
- Run similarity and hybrid search queries during calibration
- Query table stats for verification

### Setup

Supabase provides a remote HTTP MCP endpoint with OAuth authentication — no access token needed. In Cowork, it renders with an icon and Install button.

Plugin `.mcp.json` config (already bundled):

```json
{
  "supabase": {
    "type": "http",
    "url": "https://mcp.supabase.com/mcp"
  }
}
```

For manual setup in Claude Code settings (`.claude/settings.json`):

```json
{
  "mcpServers": {
    "supabase": {
      "type": "http",
      "url": "https://mcp.supabase.com/mcp"
    }
  }
}
```

On first use, you'll be prompted to authenticate via OAuth. This grants Claude access to your Supabase projects.

### Verify It Works

Ask Claude:

```
List all tables in project bihjdegxbsdpekzclyxo
```

You should see the existing `IWAI Test Database` table (184 rows). After running migrations, you'll also see `file_metadata` and `chunks`.

---

## Troubleshooting

### Supabase OAuth issues

- Try disconnecting and reconnecting the Supabase connector
- Check that your Supabase account has access to the target project

### "MCP server not found"

- Restart Claude Code / Cowork after updating settings
