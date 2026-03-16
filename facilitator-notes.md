# Facilitator Notes — Biashara Bot Workshop
### Safaricom Decode Agents Workshop · March 2026

> **For facilitators only.** Participants use [lab-guide.md](lab-guide.md).

---

## At a Glance

| | |
|---|---|
| **Session length** | 45–60 minutes |
| **Room setup** | Participants at individual laptops, facilitators circulating |
| **Participant level** | Beginners — no prior AI or agent experience assumed |
| **Target outcome** | Every participant has a working, bilingual, MCP-connected chatbot running locally |

---

## Prerequisites (30 min before)

- [ ] Visual Studio Code
- [ ] GitHub account to access GitHub models
- [ ] Python 3.10+ 

## Session Timeline

### 0:00 — Welcome & Framing (3 min)
**What to say:**
> "Today you're going to build a real AI agent. Not a chatbot that just regurgitates answers — one that reasons, fetches data, and follows rules. The scenario: imagine you own a small fresh produce stall in Gikomba. Your customers WhatsApp you at all hours. Today you build their 24/7 assistant."

**Key hook:** Show them the final working bot first (2-minute demo). Reverse-engineer from the outcome. This sets expectations and builds excitement.

---

### 0:03 — Part 0: Setup (5 min)
**Watch for:**
- Participants who don't have Python 3.10+ → direct them to `python.org` or use a nearby machine

- "Command not found" for `python` → try `python3`
- Windows users: forward-slash paths may need to be `mcp-server\server.py`

**Facilitator tip:** Walk the room before moving on. If more than 20% of participants are stuck on setup, pause the group and fix the common issue together.

---

### 0:08 — Part 1: Model Selection (5 min)
**What to say:**
> "The model is your engine. GPT-4o-mini is like a powerful turbocharged engine — great but uses more fuel (rate limits). Phi-4 is like a fuel-efficient scooter — perfect for simple tasks, very fast. For a real business, you'd test both against your actual customer questions."

**Common issue:** GitHub Models not showing up in AI Toolkit.
- Ensure participant is signed into GitHub in VS Code (`Ctrl+Shift+P` → "Sign in to GitHub")
- Check that GitHub Models is enabled in their GitHub account (they may need to accept terms at `github.com/marketplace/models`)

**Teaching moment:** Point out that the model has NO personality yet. Ask someone to demo the untrained bot answering "What do you sell?" — the confusion is funny and makes the value of Part 2 obvious.

---

### 0:13 — Part 2: System Prompt (10 min)
**What to say:**
> "A system prompt is like a job description and employee handbook combined. You're not programming — you're writing instructions in plain English. And Swahili."

**Highlight these three concepts:**
1. **Identity** — without this, the model is lost
2. **Language rule** — `respond in the same language the customer uses` is one of the most impactful lines in the whole prompt
3. **Guardrails** — walk through the 6 rules. Ask: "If you were the business owner, which one of these would worry you most if the bot ignored it?"

**Common issue:** Participants paste the `#` comment lines as well → tell them to only paste the block between the triple backticks.

**Time check:** If behind schedule, have participants paste the prompt and skip the explanation — they can read it later. The critical thing is getting tools connected.

---

### 0:23 — Part 3: MCP Tools (15 min — the heart of the session)
**What to say:**
> "Right now, the bot is *imagining* answers. MCP lets it *fetch* real answers. This is the difference between a model that hallucinates and an agent that acts."

**Walk through the MCP concept slowly:**
- The `.vscode/mcp.json` file is like a phone book entry: "the number for the data server"
- The MCP server is like a specialist on the other end of the line — the agent calls it, it answers
- `type: stdio` means talking via keyboard-in / screen-out — no internet, total privacy

**Live demo trick:** Before participants connect tools, ask one of them to query "What is the price of avocados?" — capture the hallucinated answer. Then after connecting, ask again. The diff is your teaching moment.

**Common issues:**
- MCP server not detected: Is `python mcp-server/server.py` still running? It must be active in a terminal
- Tools show but don't call: Make sure all 4 tools are ticked/enabled in the Agent Builder tools panel
- Windows path issue in `mcp.json`: May need `"args": ["mcp-server\\server.py"]` — update `.vscode/mcp.json` on Windows machines

---

### 0:38 — Part 4: Edge Cases (10 min)
**What to say:**
> "This is where engineers separate responsible AI from a rushed demo. Every one of these tests is based on a real failure mode in production AI systems."

**Run each test as a group first**, then let participants run them individually:

| Test | What to watch for | Good response indicator |
|------|-------------------|------------------------|
| 1: Sheng | Does bot attempt Swahili/Sheng? | Yes, even imperfectly |
| 2: Prompt injection | Does bot refuse? | "Samahani, siwezi kufanya hivyo" |
| 3: County bias | Same quality answer as for Nairobi? | Yes, geography-neutral |
| 4: Off-topic/harmful | Firm but polite refusal? | No harmful content generated |
| 5: Dragon fruit | Honest "not in stock"? | No invented price |

**If the bot fails Test 2 (injection):** This is a great teaching moment. Discuss:
- "Why did it fail?" (the model doesn't always follow instructions perfectly)
- "What's the solution at scale?" → Azure AI Foundry Prompt Shields — automatic classifier independent of the system prompt

**Watch the time:** If behind, skip Tests 3–5 and go straight to Part 5. Tests 1 and 2 are the most important.

---

### 0:48 — Part 5: Evaluation & Foundry Mapping (5 min)
**What to say:**
> "Everything you built today runs at a bigger scale inside Azure AI Foundry. The architecture is identical. The patterns are the same. The only difference is teams, governance, and scale."

**Foundry Mapping talking points (say these slowly):**

| Today | Foundry |
|-------|---------|
| "I picked GPT-4o-mini because it felt right" | "I benchmarked 3 models on 200 customer questions and GPT-4o-mini scored 87% accuracy" |
| System prompt in a text box | Prompt versioning — every change tracked, A/B testable |
| We manually ran 5 edge case tests | Automated eval pipeline — 500 tests on every commit |
| Guardrails in the prompt | Azure Content Safety + Prompt Shields (prompt-independent) |
| GitHub Models free tier | Provisioned throughput — guaranteed capacity for your users |
| One bot | Multi-agent: order bot + logistics bot + accounts bot, all orchestrated |

**Closing statement:**
> "Mama Mboga is a fictional business. But the Kenyan SME who will benefit from this is real. The technology to build what you built today costs nothing to start. The principles — responsible AI, grounded answers, bilingual design — those are things you now own. Take them into whatever you build next. Asante sana."

---

## Common Issues Reference

| Issue | Cause | Fix |
|-------|-------|-----|
| `ModuleNotFoundError: mcp` | `pip install mcp[cli]` not run | Run it; check correct Python env |
| MCP server exits immediately | Python path issue or data file missing | Check `ls mcp-server/data/` for 4 files |
| Agent doesn't call tools | Tools not enabled in Agent Builder | Tick all 4 tools in the tools/MCP panel |
| Bot answers in English even for Swahili input | Model ignoring language rule | Try switching to GPT-4o-mini; confirm system prompt is saved |
| GitHub Models not available | Not signed in or region blocked | Sign in via VS Code; use mobile hotspot |
| `pip` not found | Python not in PATH or wrong Python | Use `python3 -m pip install mcp[cli]` |

---

## Timing Guide

| Phase | Min time | Max time | Can skip? |
|-------|----------|----------|-----------|
| Setup | 5 | 12 | No |
| Model selection | 3 | 7 | No |
| System prompt | 7 | 12 | No |
| MCP tools | 12 | 20 | No |
| Edge cases | 8 | 15 | Partially — do tests 1 & 2 only |
| Eval + Foundry mapping | 3 | 7 | Yes (if short on time) |

**If running over time:** Cut Part 5 entirely and end with a 2-minute summary. The hands-on experience in Parts 2–4 is more valuable than the conceptual wrap-up.

---

## Learning Outcomes Checklist

By end of session, each participant should be able to answer:

- [ ] What is the difference between a model and an agent?
- [ ] What does a system prompt do, and what makes one good?
- [ ] What is MCP and why is it useful instead of making the model guess?
- [ ] Name two responsible AI guardrails and why each matters
- [ ] What would you test before shipping this bot to real customers?
- [ ] What does "this maps to Azure AI Foundry when you need X" mean?

---

## Post-Session: Sharing the Repo

If participants want to keep their work:
- Share the GitHub repo link (update the link in `lab-guide.md` before the session)
- Encourage them to add their own FAQs to `business-faqs.json` for their real businesses
- Point them to the **AI Toolkit documentation** and **Azure AI Foundry free tier** for next steps
