# 05 - Connect MCP Tools

## 1) Check MCP configuration

Open `.vscode/mcp.json` and confirm the server entry points to:

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

In VS Code, navigate to the `.vscode/mcp.json` file and click **Start** above the `biashara-bot-data-http` server to launch it.

## 2) Enable tools in Agent Builder

1. Scroll to the **Tools** section of the Agent Builder.
1. Click on the **+** icon, next to tools then select, **MCP Server > Could not find one? Browse more MCP Servers**
1. In the new tab, select **Custom** then click the **Edit** button under **mcp.json**.
1. A new **mcp.json** file will be opened, paste the following code to your file:

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
What's on the menu for breakfast and how much does it cost?
```

```text
Mnatuma chakula CBD? Delivery ni how much?
```

```text
I want to order lunch for 15 people at my office. What are your catering options?
```

The agent should now return answers grounded in actual menu data and FAQ entries instead of guessing.

## 5) Bonus Challenge: Build Your Own Tool 🛠️

The MCP server has a third data file — `mcp-server/data/market-prices.json` — that contains wholesale ingredient prices from Wakulima and Gikomba markets. **No tool exposes this data yet.** Your task is to add one.

### Goal

Create a new tool called `get_market_prices` in `mcp-server/server.py` so the agent can answer questions like:

```text
What is the current wholesale price of tomatoes?
```

```text
Which ingredients have prices that are rising?
```

```text
Compare meat prices from the market.
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
What is the wholesale price of tomatoes right now?
```

```text
Which ingredients have rising prices? Should I be worried about food costs?
```

```text
Bei ya nyama kwa jumla ni ngapi sasa hivi?
```
### Save again

Save to Local after adding the guardrails.

Continue to [06-evaluation.md](06-evaluation.md).
