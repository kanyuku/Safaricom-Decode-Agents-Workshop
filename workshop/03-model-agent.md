# 03 - Explore Models & Create the Agent

## 1) [Optional] Explore models with GitHub Copilot Agent Mode

Open **GitHub Copilot Chat** in VS Code and switch to **Agent Mode**. Ask Copilot to recommend a model for your use case:

```text
I'm building a bilingual AI customer assistant for Savanna Bites restaurant in Nairobi. It needs to handle English, Swahili, and Sheng queries about menu items, pricing, and ordering. Which model would you recommend from the AI Toolkit?
```

Review the recommendations.

For this workshop we use **gpt-4.1-mini** via custom models — it balances quality, speed, and multilingual capability.

## 2) Browse the AI Toolkit Model Catalog

<!-- TODO: Add screenshot of AI Toolkit icon in the Activity Bar -->

1. Open the **AI Toolkit** in the Activity Bar (look for the AI Toolkit icon in the left sidebar).
1. Navigate to **Developer Tools > Discover > Model Catalog**.

<!-- TODO: Add screenshot of the Model Catalog view -->


1. In the **Model Catalog**, filter by **GitHub** as the provider.
1. Find the model you want (e.g. `gpt-4.1-nano`) and click on it.
1. Click **Try in Playground** on the model card.
1. The model will load in the **Model Playground** where you can chat with it directly.
1. Do the same for gpt-4.1-mini and compare in the playground.

> **Tip:** You can open two models side-by-side in the Playground to compare their responses to the same prompt.

## 3) Create the agent in Agent Builder

<!-- TODO: Add screenshot of the Agent Builder creation flow -->

1. In AI Toolkit, go to **Developer Tools** → **+ Build** → **+ Create Agent** → **Open Agent Builder**.
1. Name the agent: `Biashara-Bot`
1. For the **Model** field, select `gpt-4.1-mini` 

## 4) Quick baseline test

Before adding a system prompt or tools, send a message:

```text
Do you have chapati and beans? How much is it?
```

The agent gives a generic answer because it has no context about the restaurant. The next sections fix this.

Continue to [04-system-prompt.md](04-system-prompt.md).
