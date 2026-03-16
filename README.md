# Biashara Bot 🥬🤖
### Build an Agentic AI Chatbot for Kenyan SMEs using VS Code AI Toolkit
**Safaricom Decode Agents Workshop · March 2026**

---

> **What you'll build:** A bilingual (English + Swahili) AI agent that acts as the 24/7 customer assistant for *Mama Mboga Fresh Supplies* — a fictional Nairobi fresh produce business. The agent uses MCP tools to fetch real business data and follows responsible AI guardrails.

---

## Session Outcomes

By the end of this workshop you will have:

1. **A fully working chatbot** enriched with Kenyan context — Swahili support, MSME-specific FAQs, and local market price awareness
2. **Responsible AI guardrails** — bias mitigation, safety layers, and prompt-injection protection, baked into the agent's system prompt
3. **A practical local-first architecture** — the whole stack runs on your laptop, with a clear pathway to cloud deployment via Azure AI Foundry

---

## Prerequisites

| Requirement | Version / Notes |
|-------------|-----------------|
| VS Code | Latest stable |
| AI Toolkit for VS Code | Install from VS Code Marketplace |
| GitHub account | Free — needed for GitHub Models access |
| Python | 3.10 or newer |
| Internet connection | For GitHub Models API calls |

---

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/your-org/Safaricom-Decode-Agents-Workshop.git
cd Safaricom-Decode-Agents-Workshop
```

### 2. Install dependencies

```bash
pip install mcp[cli]
```

### 3. Start the MCP data server

```bash
python mcp-server/server.py
```

Keep this terminal running. The server exposes four tools to your AI agent.

### 4. Open VS Code and start the workshop

Open this folder in VS Code and follow **[lab-guide.md](lab-guide.md)** step by step.

---

## Repo Structure

```
Safaricom-Decode-Agents-Workshop/
│
├── README.md                        ← You are here
├── lab-guide.md                     ← Participant step-by-step workshop guide
├── facilitator-notes.md             ← Trainer guide with timing and common issues
│
├── .vscode/
│   └── mcp.json                     ← Wires the MCP server into VS Code AI Toolkit
│
├── mcp-server/
│   ├── server.py                    ← FastMCP server exposing 4 data tools
│   ├── requirements.txt             ← Python dependency (mcp[cli])
│   └── data/
│       ├── business-faqs.json       ← FAQs for Mama Mboga Fresh Supplies
│       ├── product-catalogue.json   ← Produce catalogue with retail prices (KES)
│       ├── market-prices.json       ← Nairobi wholesale market prices & trends
│       └── kenyan-tax.json          ← KRA, VAT, Hustler Fund, business registration
│
└── agent/
    └── system-prompt.md             ← Annotated system prompt template
```

---

## The Four MCP Tools

| Tool | What it answers |
|------|-----------------|
| `search_business_faqs` | Delivery, ordering, payment (M-Pesa), hours, returns, wholesale |
| `get_product_catalogue` | In-stock produce, retail prices, farm origins |
| `get_market_prices` | Nairobi wholesale prices (Wakulima, Gikomba), seasonal trends |
| `get_tax_info` | KRA PIN, VAT, Hustler Fund, business registration, PAYE, SACCOs |

---

## Responsible AI Guardrails

The agent is built with six explicit safeguards:

| # | Guardrail | What it prevents |
|---|-----------|-----------------|
| 1 | No specific financial/legal advice | Harmful guidance to vulnerable customers |
| 2 | Equal treatment by county/ethnicity/gender | Discriminatory responses |
| 3 | Prompt injection protection | Jailbreak / "ignore instructions" attacks |
| 4 | Harmful content refusal | Offensive or dangerous output |
| 5 | Honest uncertainty ("Sijui") | Hallucinated prices or policy details |
| 6 | No political content | Brand / legal risk from political commentary |

---

## Architecture

```
Customer Message (English / Swahili / Sheng)
              ↓
  ┌─────────────────────────────────────────┐
  │      Biashara Bot                       │
  │  (VS Code AI Toolkit Agent Builder)     │
  │  Model: GitHub Models (GPT-4o-mini)     │
  │  System Prompt: identity + rules        │
  └────────────┬────────────────────────────┘
               │ MCP (stdio)
               ↓
  ┌─────────────────────────────────────────┐
  │    mcp-server/server.py (FastMCP)       │
  ├─────────────────────────────────────────┤
  │  search_business_faqs  → business-faqs.json        │
  │  get_product_catalogue → product-catalogue.json    │
  │  get_market_prices     → market-prices.json        │
  │  get_tax_info          → kenyan-tax.json           │
  └─────────────────────────────────────────┘
               ↓
  Grounded, bilingual, responsible response
```

---

## Mapping to Azure AI Foundry

This workshop uses VS Code AI Toolkit for local-first development. When you're ready to scale, the architecture maps directly to Azure AI Foundry:

| Workshop stack | Production / Foundry equivalent |
|---------------|----------------------------------|
| GitHub Models (free tier) | Azure OpenAI Service — provisioned throughput |
| System prompt in Agent Builder UI | Foundry Prompt management + version control |
| MCP server (local stdio process) | Azure Functions or Container Apps |
| Manual edge case testing | Foundry Evaluations — automated eval pipelines |
| Guardrails in system prompt | Azure AI Content Safety + Prompt Shields |
| Single agent | Multi-agent orchestration in Foundry |

---

## Workshop Flow Summary

| Part | Time | Topic |
|------|------|-------|
| 0 | 5 min | Setup — install deps, start MCP server |
| 1 | 5 min | Model selection — pick the right engine |
| 2 | 10 min | System prompt — give the bot an identity and rules |
| 3 | 15 min | MCP tools — ground the bot in real data |
| 4 | 10 min | Edge cases — test responsible AI guardrails |
| 5 | 5 min | Evaluation thinking + Foundry mapping |

---

## License

This workshop content is provided for educational purposes at the Safaricom Decode Agents Workshop.  
Fictional business data (Mama Mboga Fresh Supplies) is illustrative only.  
Tax and regulatory information is general guidance — always consult a professional.
