# 03 - Explore Models & Create the Agent

## 1) Explore models with GitHub Copilot Agent Mode

Open **GitHub Copilot Chat** in VS Code and switch to **Agent Mode**. Ask Copilot to recommend a model for your use case:

```text
I'm building a bilingual AI customer assistant for Savanna Bites restaurant in Nairobi. It needs to handle English, Swahili, and Sheng queries about menu items, pricing, and ordering. Which model would you recommend from the AI Toolkit?
```

Review the recommendations.

For this workshop we use **gpt-4.1-mini** via custom models — it balances quality, speed, and multilingual capability.

## 2) Browse the AI Toolkit Model Catalog

1. Open the **AI Toolkit** in the Activity Bar.
1. Navigate to **Developer Tools > Discover > Model Catalog**.
1. Browse available **GitHub models** and compare capabilities.
1. Try loading two models, gpt-4.1-mini and gpt-4.1-nano, in the **Model Playground** to compare their responses side-by-side.

## 3) Create the agent in Agent Builder

1. In AI Toolkit, go to **Developer Tools** → **+ Build** → **+ Create Agent** → **Open Agent Builder**.
1. Name the agent: `Biashara-Bot`
1. For the **Model** field, select `gpt-4.1-mini` 

## 4) Quick baseline test

Before adding a system prompt or tools, send a message:

```text
What's on the menu for lunch today?
```

The agent gives a generic answer because it has no context about the restaurant. The next sections fix this.

Continue to [04-system-prompt.md](04-system-prompt.md).
