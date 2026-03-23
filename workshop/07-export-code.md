# 07 - Export Agent Code & Next Steps

## 1) Export code from Agent Builder

The Agent Builder lets you export your agent as Python code that uses the **Microsoft Agent Framework**.

1. In the Agent Builder, click the **Export** button (or select **Export Code** from the menu).
2. Review the generated code — it includes your agent instructions, model configuration, and MCP tool connections.
3. The exported code uses `agent-framework` and `azure-identity` to connect to your Microsoft Foundry project.

## 2) Architecture recap

```
Customer → Agent Builder → MCP Server → JSON Data → Grounded Response
              ↓ (export)
         Python Code → Microsoft Agent Framework → Microsoft Foundry (production)
```

**Today's workshop maps to production like this:**

| Workshop | Production (Microsoft Foundry) |
|----------|-------------------------------|
| Model selected in Agent Builder | Model deployed and benchmarked against real queries |
| System prompt in a text box | Prompt versioning — every change tracked and testable |
| 4 manual evaluation rows | Automated eval pipeline with hundreds of test cases |
| AI-assisted evaluators (relevance, coherence) | Full evaluator suite with custom evaluators |
| Local MCP server with JSON data | Production MCP server with database backend |
| Single agent | Multi-agent orchestration |

## 3) Suggested next steps

1. **Add more evaluation rows** — expand your test set with 10–20 prompts covering diverse customer scenarios
2. **Add a new FAQ** in `mcp-server/data/business-faqs.json` (e.g. WiFi availability, parking)
3. **Add a new tool** in `mcp-server/server.py` (e.g. `check_wait_time` or `get_daily_special`)
4. **Deploy to Microsoft Foundry** — use the exported code as a starting point for a cloud-hosted agent
5. **Explore Responsible AI** — add [Azure AI Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/overview) for production guardrails

## Resources

| Resource | Link |
|----------|------|
| AI Toolkit | https://aka.ms/AIToolkit |
| Microsoft Foundry | https://ai.azure.com/ |
| GitHub Copilot Agent Mode | https://code.visualstudio.com/docs/copilot/chat/chat-agent-mode |
| Azure AI Content Safety | https://learn.microsoft.com/azure/ai-services/content-safety/overview |
| BRK441 Reference Repo | https://github.com/microsoft/aitour26-BRK441-Build-and-launch-AI-agents-fast-with-Microsoft-Foundry-and-the-AI-Toolkit |

Done! 🎉
