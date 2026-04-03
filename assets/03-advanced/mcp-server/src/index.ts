import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { validateEnv } from "./lib/supabase.js";
import { searchKbSchema, SEARCH_KB_DESCRIPTION, handleSearchKb } from "./tools/search-kb.js";
import { LIST_SOURCES_DESCRIPTION, handleListSources } from "./tools/list-sources.js";

// Validate environment variables before starting
try {
  validateEnv();
} catch (err: any) {
  console.error(`[kb-search] Startup error: ${err.message}`);
  process.exit(1);
}

const server = new McpServer({
  name: "kb-search",
  version: "1.0.0",
});

// Register search_kb tool
server.tool(
  "search_kb",
  SEARCH_KB_DESCRIPTION,
  searchKbSchema,
  async (args) => {
    try {
      const result = await handleSearchKb(args);
      return { content: [{ type: "text", text: result }] };
    } catch (err: any) {
      return {
        content: [{ type: "text", text: `Error: ${err.message}` }],
        isError: true,
      };
    }
  }
);

// Register list_sources tool
server.tool(
  "list_sources",
  LIST_SOURCES_DESCRIPTION,
  {},
  async () => {
    try {
      const result = await handleListSources();
      return { content: [{ type: "text", text: result }] };
    } catch (err: any) {
      return {
        content: [{ type: "text", text: `Error: ${err.message}` }],
        isError: true,
      };
    }
  }
);

// Start stdio transport
const transport = new StdioServerTransport();
await server.connect(transport);
