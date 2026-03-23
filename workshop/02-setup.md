# 02 - Setup

## 1) Confirm VS Code extensions

Open VS Code and install the following extensions are installed:

- [AI Toolkit](https://aka.ms/AIToolkit) (includes Microsoft Foundry)
- [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)

## 2) Access to models

1. Head over to event link: *## will be added day of the event*
1. Follow the instructions to generate your API Key
1. Once you get your Event API keys, follow the next set of instructions to add your models to AI Toolkit

## 2) Add models to AI Toolkit
1. Open the **AI Toolkit** extension in the Activity Bar.
1. Go to **My resources > connected resources** in the pop-up select **Add Custom Model**.
1. In the next pop-up, go back to the event.link and copy the **Endpoint**, then click enter
1. In the next pop-up, go back to the event.link and copy the **Model**, then click enter
1. In the next pop-up, leave model name as is, then click enter.
1. In the next pop-up, go back to the event link and copy the **Event API Key**, then click enter.
1. A pop up will appear on your left with the following title, **Model added successfully. Try the model in the playground.**

## 4) Install Python dependencies

```bash
pip install -r requirements.txt
```

If needed, use `pip3` instead of `pip`.

## 5) Start the MCP server

```bash
python mcp-server/server.py
```

Keep this terminal running.

## 6) Verify data files

```bash
ls mcp-server/data/
```

Expected files:
- `business-faqs.json`
- `product-catalogue.json`

Continue to [03-model-agent.md](03-model-agent.md).
