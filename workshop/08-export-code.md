# 08 - Export Agent Code & Next Steps

## 1) Why export to a Framework?

The Agent Builder is a prototyping environment — great for iterating on prompts, tools, and evaluations. But to ship Biashara Agent to real customers (WhatsApp, a website, an internal dashboard), you need **standalone code** that can run on a server, scale, and be version-controlled.

Exporting gives you:

- **A Python project** you can commit to GitHub and review in PRs
- **Reproducible deployments** — the same agent runs identically every time
- **Integration flexibility** — embed the agent in any app (Flask, FastAPI, WhatsApp webhook, etc.)
- **A path to Microsoft Foundry** — the exported code uses the Agent Framework SDK, which plugs directly into Foundry for production hosting, monitoring, and multi-agent orchestration

## 2) Export code from Agent Builder

<!-- TODO: Add screenshot of the View Code button in Agent Builder -->

1. In the Agent Builder, click the **View Code** button (top-right corner of the Agent Builder panel).

    - **SDK**: Microsoft Agent Framework
    - **Programming Language**: Python
    - Save file.

1. The exported code uses the **Microsoft Agent Framework** SDK and authenticates via `azure-identity` (DefaultAzureCredential) to connect to your Microsoft Foundry project.

> **Note:** The exported code is a starting point, not a finished product. You'll customise it for your deployment target.

## 3) From workshop to production

Everything you built today in AI Toolkit has a production-grade equivalent in Microsoft Foundry:

| What we did in AI Toolkit | What you can do in Microsoft Foundry |
|---------------------------|--------------------------------------|
| Selected `gpt-4.1-mini` from the Model Catalog | Deploy and manage models with usage quotas, rate limits, and automatic failover |
| Wrote a system prompt in the Instructions field | Instructions and system prompts in Foundry |
| Connected a local MCP server with JSON data files | Connect production MCP servers backed by databases, APIs, and live services |
| Ran 5 manual evaluation rows in the Evaluation tab | Run automated evaluation pipelines with hundreds of test cases on every commit |
| Scored responses with relevance and coherence evaluators | Use the full evaluator suite — groundedness, fluency, safety — plus custom evaluators |
| Tested prompt injection attacks in chat | Apply Azure AI Content Safety filters and Responsible AI dashboards at the platform level |
| Built a single agent | Orchestrate multiple agents (e.g. order bot + delivery bot + accounts bot) |
| Chatted at localhost:5000 | Host agents on a scalable endpoint using Hosted Agents and connect WhatsApp, web widgets, or mobile apps |
| Exported code via **View Code** | Deploy that code directly to Foundry Hosted Agents with built-in monitoring |

### What a production deployment looks like

1. **Push your exported code** to a GitHub repository
2. **Connect to Microsoft Foundry** — deploy the agent to a cloud-hosted endpoint with built-in scaling
3. **Add a front-end** — connect the Foundry Hosted Agents endpoint to WhatsApp (via Twilio or Africa's Talking), a website chat widget, or an internal tool
4. **Set up CI/CD evaluations** — run your evaluation suite on every code change to catch regressions before they reach customers
5. **Monitor with Application Insights** — track response quality, latency, and tool usage in production

## 4) Suggested next steps

**Improve the agent:**
1. **Add more evaluation rows** — expand your test set with 10–20 prompts covering diverse customer scenarios
1. **Add a new FAQ** in `mcp-server/data/business-faqs.json` (e.g. WiFi availability, parking)
1. **Add a new tool** in `mcp-server/server.py` (e.g. `check_wait_time` or `get_daily_specials`)

**Take it to production:**
1. **Deploy to Microsoft Foundry** — use the exported code as a starting point for a cloud-hosted agent
1. **Add a customer channel** — connect the agent to WhatsApp, a website widget using hosted agents
1. **Explore Responsible AI** — add [Azure AI Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/overview) for production guardrails

## Resources

| Resource | Link |
|----------|------|
| AI Toolkit | https://aka.ms/AIToolkit |
| Microsoft Foundry | https://ai.azure.com/ |
| GitHub Copilot Agent Mode | https://code.visualstudio.com/docs/copilot/chat/chat-agent-mode |
| Azure AI Content Safety | https://learn.microsoft.com/azure/ai-services/content-safety/overview |
| BRK441 Reference Repo | https://github.com/microsoft/aitour26-BRK441-Build-and-launch-AI-agents-fast-with-Microsoft-Foundry-and-the-AI-Toolkit |

Done! 🎉
