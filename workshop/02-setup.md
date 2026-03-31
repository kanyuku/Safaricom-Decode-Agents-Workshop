# 02 - Setup

## 1) Confirm VS Code extensions

Open VS Code and ensure the following extensions are installed:

- [AI Toolkit](https://aka.ms/AIToolkit)
- [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)

## 2) Access to models

1. Head over to the event link: [https://gray-wave-002399710.1.azurestaticapps.net/event/3268-88a1](https://gray-wave-002399710.1.azurestaticapps.net/event/3268-88a1).
1. Follow the instructions to generate your API Key
1. Once you get your Event API keys, follow the next set of instructions below to add your models to AI Toolkit

## 3) Add models to AI Toolkit

1. Open the **AI Toolkit** extension in the Activity Bar.
1. Go to **My resources > connected resources**, hover on **Models** and click on the **+** sign. Select **Add Custom Model**.
1. **Endpoint URL.** Copy the **gpt-4.1-mini Endpoint** value from the event.link, paste it here, then click enter
1. **Model name.** Copy the **Model** value from the event.link, paste it here, then click enter
1. **Display model name.** Leave default model name as is, then click enter.
1. **API Key.** Copy the **Event API Key** value from the event.link, paste it here, then click enter
1. A pop up will appear on your right with the following title, **Model added successfully. Try the model in the playground.**

## 4) Install Python dependencies

Create and activate a virtual environment, then install the dependencies:

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

If needed, use `python3` instead of `python`.

## 5) Start the MCP server

```bash
python mcp-server/server.py
```

You should see output like:

```
Starting Biashara Agent MCP Data Server (HTTP)...
📡 MCP endpoint available at: http://127.0.0.1:8000/mcp
Tools available: search_business_faqs, get_product_catalogue
```

Keep this terminal running.

Continue to [03-model-agent.md](03-model-agent.md).
