# Biashara Agent Workshop

Build a bilingual (English, Swahili), AI assistant for Savanna Bites restaurant (Nairobi), using **Microsoft Foundry** and the **AI Toolkit** in VS Code.

## Start Here

1. Open [workshop/01-overview.md](workshop/01-overview.md) for prerequisites and session goals.
1. Follow the participant guide in [lab-guide.md](lab-guide.md).
1. Use [workshop/README.md](workshop/README.md) for section-by-section flow.

## Key Files

- [lab-guide.md](lab-guide.md): Participant index and sequence
- [workshop/](workshop/README.md): Split workshop sections
- [agent/system-prompt.md](agent/system-prompt.md): Agent instructions template
- [facilitator-notes.md](facilitator-notes.md): Trainer notes

## Workshop Flow

1. **Explore & Compare Models** — use GitHub Copilot Agent Mode and AI Toolkit Model Catalog
1. **Create Agent** — set up Biashara Agent in Agent Builder with `gpt-4.1-mini` via Microsoft Foundry
1. **System Prompt** — define the agent's personality, role, and language behaviour
1. **MCP Tools** — connect the local data server for grounded answers
1. **Evaluation** — run manual and AI-assisted evaluations on agent responses
1. **Web App** — deploy a Flask chat interface powered by the agent
1. **Export Code** — export agent code for production with Microsoft Agent Framework

## Getting Started

### Fork this repo

1. [Fork](https://github.com/BethanyJep/Safaricom-Decode-Agents-Workshop/fork) this repository
1. Clone your fork locally:

```bash
git clone https://github.com/<your-username>/Safaricom-Decode-Agents-Workshop.git
cd Safaricom-Decode-Agents-Workshop
```

1. Open the folder in VS Code:

```bash
code .
```

Then follow the workshop steps starting at [workshop/01-overview.md](workshop/01-overview.md).

## Additional Resources

1. [BRK441: Build and launch AI agents fast with Microsoft Foundry and the AI Toolkit](https://github.com/microsoft/aitour26-BRK441-Build-and-launch-AI-agents-fast-with-Microsoft-Foundry-and-the-AI-Toolkit)