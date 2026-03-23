# 05 - Connect MCP Tools

## 1) Check MCP configuration

Open `.vscode/mcp.json` and confirm the server entry points to:

```json
{
  "servers": {
    "biashara-bot-data": {
      "type": "stdio",
      "command": "python",
      "args": ["mcp-server/server.py"],
      "env": {}
    }
  }
}
```

In VS Code, navigate to the `.vscode/mcp.json` file and click **Start** above the `biashara-bot-data` server to launch it.

## 2) Enable tools in Agent Builder

Scroll to the **Tools** section of the Agent Builder. Enable:

- `search_business_faqs`
- `get_product_catalogue`

## 3) Save this version

Clear the chat window, then at the bottom of the Agent Builder select **Save Version**. Name it `v2-tools-agent`.

## 4) Test with grounded queries

Now ask questions that require real data:

```text
What do you have for breakfast and how much does it cost?
```

```text
Mnatuma chakula CBD? Na bei ya utoaji ni ngapi?
```

```text
I want to order lunch for 15 people at my office. What are your catering options?
```

The agent should now return answers grounded in actual menu data and FAQ entries instead of guessing.

Continue to [06-evaluation.md](06-evaluation.md).
