"""
Biashara Agent — Chat Web App
============================
A Flask web app that lets you chat with the Savanna Bites Restaurant AI agent.

The app connects to GitHub Models (or any OpenAI-compatible endpoint) for the LLM
and reuses the MCP server's JSON data files for tool responses.

Usage:
  1. Set your GITHUB_TOKEN:  export GITHUB_TOKEN="your-token"
  2. Start the app:          python webapp/app.py
  3. Open in browser:        http://127.0.0.1:5000
"""

import json
import os
import uuid

from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from openai import OpenAI

load_dotenv()

app = Flask(__name__)

# --------------- Configuration ---------------
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
MODEL = os.environ.get("MODEL", "gpt-4.1-mini")
ENDPOINT = os.environ.get("ENDPOINT", "https://models.github.ai/inference")

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "mcp-server", "data")

SYSTEM_PROMPT = (
    "You are Biashara Agent, an intelligent and friendly AI assistant for "
    "Savanna Bites Restaurant in Nairobi CBD. You help customers with their "
    "dining needs by understanding what they are looking for and recommending "
    "the most suitable items from the menu.\n\n"
    "Your role is to:\n"
    "- Engage with the customer in natural conversation to understand what they need.\n"
    "- Ask thoughtful questions to gather relevant details.\n"
    "- Be brief in your responses.\n"
    "- Provide the best solution for the customer's question and only recommend "
    "items within Savanna Bites' menu.\n"
    "- Search the restaurant's product catalogue to identify items that best match "
    "the customer's needs.\n"
    "- Clearly explain what each recommended item is, why it's a good fit, and "
    "how much it costs.\n"
    "- Reply in the user's language (English, Swahili, or mixed/Sheng).\n\n"
    "Your personality is:\n"
    "- Warm and welcoming, like a friendly waiter\n"
    "- Professional and knowledgeable, like a seasoned restaurant host\n"
    "- Curious and conversational — never assume, always clarify\n"
    "- Transparent and honest — if something isn't available, offer support anyway\n\n"
    "If no matching items are found in the catalogue, say:\n"
    '"Thanks for sharing those details! I\'ve searched our menu, but it looks like '
    "we don't currently have something that fits your exact request. If you'd like, "
    'I can suggest some alternatives or help you find something similar."\n\n'
    "## Safety guardrails\n\n"
    "- Only discuss topics related to Savanna Bites Restaurant: menu items, prices, "
    "delivery, catering, and restaurant information.\n"
    "- Do not generate, link to, or discuss content that is harmful, hateful, or illegal."
)

# --------------- Data helpers (mirrors mcp-server/server.py logic) ---------------


def _load(filename: str) -> dict:
    with open(os.path.join(DATA_DIR, filename), "r", encoding="utf-8") as f:
        return json.load(f)


def search_business_faqs(query: str) -> str:
    data = _load("business-faqs.json")
    query_words = query.lower().split()
    matches = []
    for faq in data["faqs"]:
        searchable = " ".join([
            faq.get("question", ""),
            faq.get("answer", ""),
            faq.get("question_sw", ""),
            faq.get("answer_sw", ""),
            " ".join(faq.get("keywords", [])),
        ]).lower()
        if any(word in searchable for word in query_words):
            matches.append(
                f"**Q: {faq['question']}**\n"
                f"A: {faq['answer']}\n\n"
                f"*(Kwa Kiswahili)* {faq.get('answer_sw', '')}"
            )
    if not matches:
        return (
            "Hakuna majibu yaliyopatikana kwa swali hilo.\n"
            "No FAQs matched your query. Try keywords like: "
            "delivery, payment, order, menu, contact, hours."
        )
    business = data["business"]
    header = (
        f"Business: {business['name']}\n"
        f"Phone/WhatsApp: {business['phone']} | "
        f"M-Pesa Paybill: {business['mpesa_paybill']} (Acc: {business['mpesa_account']})\n"
        f"Hours: {business['hours']['weekdays']} | {business['hours']['sunday']}\n"
        "--------------------------------------------------\n"
    )
    return header + "\n\n".join(matches)


def get_product_catalogue(category: str = "all") -> str:
    data = _load("product-catalogue.json")
    lines = [
        f"Product Catalogue — {data['business']}",
        f"Updated: {data['last_updated']} | Currency: {data['currency']}",
        f"Note: {data['note']}",
        "=" * 50,
    ]
    for cat in data["categories"]:
        if category == "all" or category.lower() in cat["name"].lower():
            lines.append(f"\n--- {cat['name']} ({cat['name_sw']}) ---")
            for p in cat["products"]:
                stock = "✓ In stock" if p["in_stock"] else "✗ Out of stock"
                seasonal = " [Seasonal]" if p["seasonal"] else ""
                lines.append(
                    f"  {p['name_en']} / {p['name_sw']}: "
                    f"KES {p['price']} per {p['unit']} — {stock}{seasonal}"
                )
                lines.append(f"    Origin: {p.get('origin', 'N/A')} | {p['description']}")
    if len(lines) <= 4:
        available = [c["name"].lower() for c in data["categories"]]
        return (
            f"Category '{category}' not found.\n"
            f"Available categories: {', '.join(available)}, or 'all'."
        )
    return "\n".join(lines)


def get_daily_specials(category: str = "all") -> str:
    data = _load("daily-specials.json")
    lines = [
        f"Daily Specials & Offers — {data['business']}",
        f"Note: {data['note']}",
        "=" * 50,
    ]
    cat_lower = category.lower()
    if cat_lower in ["all", "specials", "daily"]:
        lines.append("\n--- Weekly Daily Specials ---")
        for s in data["daily_specials"]:
            price_str = (
                f"KES {s['special_price']}" if s["special_price"] else "See details"
            )
            lines.append(
                f"  {s['day']} ({s['day_sw']}): {s['name_en']} / {s['name_sw']} — {price_str}"
            )
            lines.append(f"    {s['description']} (Available: {s['available']})")
    if cat_lower in ["all", "combos", "combo"]:
        lines.append("\n--- Combo Deals (Every Day) ---")
        for c in data["combo_deals"]:
            lines.append(
                f"  {c['name_en']} / {c['name_sw']}: KES {c['combo_price']} (Save KES {c['saving']})"
            )
            lines.append(f"    {c['description']} (Available: {c['available']})")
    if cat_lower in ["all", "promotions", "promo"]:
        lines.append("\n--- Active Promotions ---")
        for p in data["promotions"]:
            lines.append(f"  {p['name_en']} / {p['name_sw']}")
            lines.append(f"    {p['description']}")
            lines.append(f"    Validity: {p['valid_from']} to {p['valid_to']}")
    return "\n".join(lines)


# --------------- OpenAI tool definitions ---------------

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_business_faqs",
            "description": (
                "Search Savanna Bites Restaurant FAQs. Use this tool to answer questions about: "
                "delivery areas and fees, how to place an order, payment methods (M-Pesa, cash, card), "
                "opening hours and meal times, catering and event orders, dietary options and allergies, "
                "loyalty programme and reservations, complaints and refunds, contact details."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The customer's question or keywords to search for.",
                    }
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_product_catalogue",
            "description": (
                "Get the current menu and prices for Savanna Bites Restaurant. Use this tool to answer "
                "questions about: what meals and snacks are available, current prices (in KES), "
                "whether an item is in stock, whether an item is seasonal, meal descriptions and ingredients."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "Filter by category. Options: 'breakfast', 'lunch', 'snacks', 'drinks', or 'all' (default).",
                        "default": "all",
                    }
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_daily_specials",
            "description": (
                "Get today's daily specials, combo deals, and active promotions. Use this tool to answer "
                "questions about: today's special meal and its price, lunch combo deals, weekly promotions, "
                "loyalty club offers, group deals and catering discounts."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "Filter by category. Options: 'specials', 'combos', 'promotions', or 'all' (default).",
                        "default": "all",
                    }
                },
                "required": [],
            },
        },
    },
]

TOOL_FUNCTIONS = {
    "search_business_faqs": search_business_faqs,
    "get_product_catalogue": get_product_catalogue,
    "get_daily_specials": get_daily_specials,
}

# --------------- In-memory conversation store ---------------

conversations: dict[str, list[dict]] = {}

# --------------- Routes ---------------


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "Missing 'message' field"}), 400

    session_id = data.get("session_id") or str(uuid.uuid4())
    user_message = data["message"].strip()
    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    if session_id not in conversations:
        conversations[session_id] = [{"role": "system", "content": SYSTEM_PROMPT}]

    conversations[session_id].append({"role": "user", "content": user_message})

    client = OpenAI(base_url=ENDPOINT, api_key=GITHUB_TOKEN)

    # Agentic tool-calling loop (max 5 rounds to prevent runaway)
    for _ in range(5):
        response = client.chat.completions.create(
            model=MODEL,
            messages=conversations[session_id],
            tools=TOOLS,
        )
        choice = response.choices[0]
        assistant_msg = choice.message

        # Append assistant message to history
        conversations[session_id].append(assistant_msg.model_dump())

        if not assistant_msg.tool_calls:
            break

        # Execute each tool call
        for tool_call in assistant_msg.tool_calls:
            fn_name = tool_call.function.name
            fn = TOOL_FUNCTIONS.get(fn_name)
            if fn is None:
                tool_result = f"Unknown tool: {fn_name}"
            else:
                args = json.loads(tool_call.function.arguments)
                tool_result = fn(**args)

            conversations[session_id].append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": tool_result,
            })

    return jsonify({
        "response": assistant_msg.content or "",
        "session_id": session_id,
    })


@app.route("/api/reset", methods=["POST"])
def reset():
    data = request.get_json() or {}
    session_id = data.get("session_id")
    if session_id and session_id in conversations:
        del conversations[session_id]
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    if not GITHUB_TOKEN:
        print("⚠️  GITHUB_TOKEN is not set. Export it first:")
        print("   export GITHUB_TOKEN='your-github-token'")
        print("   Then re-run: python webapp/app.py")
        exit(1)
    print(f"🍽️  Biashara Agent Web App starting...")
    print(f"   Model: {MODEL}")
    print(f"   Endpoint: {ENDPOINT}")
    print(f"   Open http://127.0.0.1:5000 in your browser")
    app.run(debug=True, port=5000)
