# Facilitator Notes — Biashara Bot Workshop
### Safaricom Decode Agents Workshop · March 2026

> **For facilitators only.** Participants use [lab-guide.md](lab-guide.md).
>
> Based on [BRK441: Build and launch AI agents fast with Microsoft Foundry and the AI Toolkit](https://github.com/microsoft/aitour26-BRK441-Build-and-launch-AI-agents-fast-with-Microsoft-Foundry-and-the-AI-Toolkit)

---

## At a Glance

| | |
|---|---|
| **Session length** | 45–60 minutes |
| **Room setup** | Participants at individual laptops, facilitators circulating |
| **Participant level** | Beginners — no prior AI or agent experience assumed |
| **Target outcome** | Every participant has a working, bilingual, MCP-connected agent running in AI Toolkit with evaluations |

---

## Prerequisites (30 min before)

- [ ] Visual Studio Code with AI Toolkit extension
- [ ] GitHub account with GitHub Copilot subscription
- [ ] Python 3.10+
- [ ] Azure subscription with a Microsoft Foundry project
- [ ] `gpt-4.1-mini` model deployed in the Foundry project

## Session Timeline

### 0:00 — Welcome & Framing (3 min)
**What to say:**
> "Today you're going to build a real AI agent — not a chatbot that just regurgitates answers, but one that reasons, fetches data, and follows rules. The scenario: Savanna Bites Restaurant in Nairobi CBD needs a 24/7 bilingual assistant. You'll build it using Microsoft Foundry and the AI Toolkit."

**Key hook:** Show them the final working bot first (2-minute demo). Reverse-engineer from the outcome. This sets expectations and builds excitement.

---

### 0:03 — Part 0: Setup (5 min)
**Watch for:**
- Participants who don't have Python 3.10+ → direct them to `python.org` or use a nearby machine
- AI Toolkit extension not installed → install from VS Code marketplace
- Azure sign-in issues → help with `az login` or Azure Resources extension sign-in
- Microsoft Foundry project not set as default → walk them through the Azure Resources → Microsoft Foundry setup

**Facilitator tip:** Walk the room before moving on. If more than 20% of participants are stuck on setup, pause the group and fix the common issue together.

---

### 0:08 — Part 1: Model Exploration & Agent Creation (8 min)
**What to say:**
> "First, we'll use GitHub Copilot Agent Mode to get model recommendations, then browse the AI Toolkit Model Catalog. Our model today is gpt-4.1-mini via Microsoft Foundry — a good balance of quality, speed, and multilingual capability."

**Common issue:** GitHub Copilot not available.
- Ensure participant is signed into GitHub in VS Code (`Ctrl+Shift+P` → "Sign in to GitHub")
- Must have a GitHub Copilot subscription

**Teaching moment:** Point out that the model has NO personality yet. Ask someone to demo the untrained bot answering "What do you sell?" — the confusion is funny and makes the value of Part 2 obvious.

---

### 0:16 — Part 2: System Prompt (8 min)
**What to say:**
> "The instructions field is like a job description and employee handbook combined. You're not programming — you're writing instructions in plain language."

**Highlight these concepts:**
1. **Identity** — without this, the model is lost
1. **Language rule** — `reply in the user's language` is one of the most impactful lines
1. **Personality** — warm, professional, honest, conversational
1. **Save to Local** — emphasise version control.

**Common issue:** Participants paste incorrectly → tell them to only paste the block between the triple backticks.

**Time check:** If behind schedule, have participants paste the prompt and skip the explanation — they can read it later. The critical thing is getting tools connected.

---

### 0:24 — Part 3: MCP Tools (12 min — the heart of the session)
**What to say:**
> "Right now, the bot is *imagining* answers. MCP lets it *fetch* real answers. This is the difference between a model that hallucinates and an agent that acts."

**Walk through the MCP concept:**
- The `.vscode/mcp.json` file tells the Agent Builder where the data server is
- The MCP server is like a specialist on the other end — the agent calls it, it answers
- `type: http` means local HTTP communication — the server runs at `http://127.0.0.1:8000/mcp`


**Remind participants to save:** After connecting tools, save agent.

**Common issues:**
- MCP server not detected: Is `python mcp-server/server.py` still running? It must be active
- Tools show but don't call: Make sure tools are enabled in the Agent Builder tools panel
- Windows path issue: May need `"args": ["mcp-server\\server.py"]` in `mcp.json`

---

### 0:36 — Part 4: Evaluation (12 min)
**What to say:**
> "In a real project, you don't ship an agent by 'it seems to work'. You write test cases and run them. The AI Toolkit lets you do manual evaluation AND AI-assisted evaluation right inside the Agent Builder."

**Manual evaluation:**
1. Walk through adding 4 test rows in the Evaluation tab
1. Run responses and review them.

**AI-assisted evaluation:**
1. Add an evaluation with `relevance` and `coherence` evaluators
1. Select `gpt-4.1-mini` as the evaluator model
1. Run and review scores.

> **Note:** The first run of AI-assisted evaluations downloads dependencies — warn participants this may take a moment.

**GitHub Copilot tip:** Show participants they can ask Copilot Agent Mode for evaluator recommendations.

---

### 0:48 — Part 5: Export Code & Next Steps (5 min)
**What to say:**
> "Everything you built today can be exported as Python code using the Microsoft Agent Framework. The Agent Builder is your prototyping tool — Microsoft Foundry is your production platform."

**Production mapping talking points:**

| Today | Production (Microsoft Foundry) |
|-------|-------------------------------|
| Model selected in Agent Builder | Benchmarked across 200+ customer questions |
| Instructions in a text box | Prompt versioning — every change tracked, A/B testable |
| 4 manual test rows | Automated eval pipeline — hundreds of tests on every commit |
| Local MCP server | Production MCP server with database backend |
| AI-assisted evaluators | Full evaluator suite with custom evaluators |
| Single agent | Multi-agent: order bot + logistics bot + accounts bot |

**Closing statement:**
> "The technology to build what you built today costs nothing to start. The patterns — grounded answers, bilingual design, structured evaluation — those are things you now own. Take them into whatever you build next. Asante sana."

---

## Common Issues Reference

| Issue | Cause | Fix |
|-------|-------|-----|
| `ModuleNotFoundError: mcp` | `pip install mcp[cli]` not run | Run it; check correct Python env |
| MCP server exits immediately | Python path issue or data file missing | Check `ls mcp-server/data/` for files |
| Agent doesn't call tools | Tools not enabled in Agent Builder | Tick tools in the tools/MCP panel |
| Bot answers in English even for Swahili input | Model ignoring language rule | Confirm instructions are saved; try gpt-4.1-mini |
| GitHub Copilot not available | Not signed in or no subscription | Sign in via VS Code; needs Copilot subscription |
| `pip` not found | Python not in PATH or wrong Python | Use `python3 -m pip install mcp[cli]` |
| Azure sign-in fails | Wrong tenant or expired token | Run `az login --tenant {your-tenant}` |
| AI-assisted eval fails | Port conflict or dependencies not installed | Stop other local servers; let dependencies download |

---

## Timing Guide

| Phase | Min time | Max time | Can skip? |
|-------|----------|----------|-----------|
| Setup | 5 | 10 | No |
| Model exploration & agent creation | 5 | 10 | No |
| System prompt | 5 | 10 | No |
| MCP tools | 10 | 15 | No |
| Evaluation (manual + AI-assisted) | 8 | 15 | Partially — do manual only |
| Export code & next steps | 3 | 7 | Yes (if short on time) |

**If running over time:** Cut Part 5 entirely and end with a 2-minute summary. The hands-on experience in Parts 2–4 is more valuable than the conceptual wrap-up.

---

## Learning Outcomes Checklist

By end of session, each participant should be able to answer:

- [ ] What is the difference between a model and an agent?
- [ ] What does a system prompt / agent instructions do, and what makes one good?
- [ ] What is MCP and why is it useful instead of making the model guess?
- [ ] How do you run manual and AI-assisted evaluations in Agent Builder?
- [ ] What would you test before shipping this bot to real customers?
- [ ] How does the workshop map to Microsoft Foundry for production?

---

## Post-Session: Sharing the Repo

If participants want to keep their work:
- Share the GitHub repo link (update the link in `lab-guide.md` before the session)
- Encourage them to add their own FAQs to `business-faqs.json` for their real businesses
- Point them to the **AI Toolkit documentation** and **Microsoft Foundry** for next steps
- Share the BRK441 reference repo: https://github.com/microsoft/aitour26-BRK441-Build-and-launch-AI-agents-fast-with-Microsoft-Foundry-and-the-AI-Toolkit
