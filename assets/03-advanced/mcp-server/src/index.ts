import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { validateEnv } from "./lib/supabase.js";
import { searchKbTool, handleSearchKb } from "./tools/search-kb.js";
import { listSourcesTool, handleListSources } from "./tools/list-sources.js";

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
  searchKbTool.name,
  searchKbTool.description,
  searchKbTool.inputSchema.properties,
  async (args) => {
    try {
      const result = await handleSearchKb(args as any);
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
  listSourcesTool.name,
  listSourcesTool.description,
  listSourcesTool.inputSchema.properties,
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
