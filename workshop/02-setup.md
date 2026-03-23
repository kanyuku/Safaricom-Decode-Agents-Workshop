# 02 - Setup

## 1) Confirm VS Code extensions

Open VS Code and verify the following extensions are installed:

- [AI Toolkit](https://aka.ms/AIToolkit) (includes Microsoft Foundry)
- [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
- [Azure Resources](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-azureresourcegroups)

> The Azure Resources extension is bundled with the Microsoft Foundry extension in AI Toolkit.

## 2) Sign in to Azure

1. Open the **Azure Resources** extension in the Activity Bar.
2. Select **Sign in to Azure**.
3. Sign in with the account that has your Microsoft Foundry project and `gpt-4.1-mini` deployment.

## 3) Set your default Foundry project

1. In the Azure Resources extension, expand your subscription and then **Microsoft Foundry**.
2. Right-click your project name and select **Open in Microsoft Foundry Extension**.
3. If the project is not set as default, hover over the project name in the Microsoft Foundry extension and click the **Switch Default Project** icon.

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
