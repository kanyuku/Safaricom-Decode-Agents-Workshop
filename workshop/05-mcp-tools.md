# 05 - Connect MCP Tools

## 1) MCP overview

> **What is MCP?** MCP (Model Context Protocol) is an open standard that lets AI agents call external tools and data sources. Instead of the model guessing or hallucinating answers, MCP lets it *fetch* real data from a server you control. Think of it as giving your agent a phone it can use to call a specialist.

## 2) Enable tools in Agent Builder

<!-- TODO: Add screenshot of the Tools section in Agent Builder -->

1. Scroll to the **Tools** section of the Agent Builder.
1. Click on the **+** icon, next to tools then select, **MCP Server > Could not find one? Browse more MCP Servers**
1. In the new tab, select **Custom** then click the **Edit** button under **mcp.json**.
1. A new **mcp.json** file will open — this is the AI Toolkit's own MCP config (separate from the `.vscode/mcp.json` in the workspace). Paste the following code into this file:

```json
{
  "servers": {
    "biashara-bot-data-http": {
      "url": "http://127.0.0.1:8000/mcp",
      "type": "http"
    }
  },
  "inputs": []
}

```

Back on the Agent Builder, in the **Tools** section, click on the **+** icon, next to tools then select **biashara-bot-data-http** MCP Server.

## 3) Test with grounded queries

 Now ask questions that require grounded data:

```text
Nina mtu mgeni kutoka nje — recommend something authentically Kenyan for lunch.
```

```text
Ninalipa na M-Pesa. Paybill ni gani na account number?
```

```text
Do you have any vegetarian options? I'm allergic to gluten too.
```

The agent should now return answers grounded in actual menu data and FAQ entries instead of guessing.

## 4) Bonus Challenge: Build Your Own Tool 🛠️

The MCP server has a third data file — `mcp-server/data/daily-specials.json` — that contains today's daily specials, combo deals, and current promotions at Savanna Bites. **No tool exposes this data yet.** Your task is to add one.

### Goal

Create a new tool called `get_daily_specials` in `mcp-server/server.py` so the agent can answer questions like:

```text
What's today's special at Savanna Bites?
```

```text
Do you have any combo deals for lunch?
```

```text
Kuna offers zozote wiki hii?
```

### Step-by-step

1. **Open** `mcp-server/server.py` in VS Code.

2. **Add a new tool** after the existing `get_product_catalogue` tool (before the `# Entry point` section). Use the same patterns you see in the existing tools.

3. **Restart the MCP server** — stop the running server (<kbd>Ctrl+C</kbd>) and start it again:

```bash
cd mcp-server
python server.py
```

4. **Restart the MCP connection** in VS Code — open `.vscode/mcp.json` and click **Stop** then **Start** on the server entry so the Agent Builder picks up the new tool.

    In Agent Builder, delete the MCP Server, and the re-add it to refresh the tool list. You should now see 3 tools available.

5. **Test it** — ask the agent these questions and verify it uses your new tool:

```text
I'm coming in on Friday — any special deals?
```

```text
Is there a good deal for a group of four on Saturday?
```

```text
Mna promotion yoyote ya delivery wiki hii?
```
### Save again

Save to Local after adding the new tool.

Continue to [06-evaluation.md](06-evaluation.md).
