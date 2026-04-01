"""
Savanna Bites Restaurant — Biashara Agent MCP Data Server
=======================================================
A FastMCP server that exposes business data for the Biashara Agent AI agent.
Participants: you do NOT need to edit this file during the workshop.
Just run it, then configure your AI Toolkit agent to use it.

Supports two transport modes:
  stdio: python mcp-server/server.py --stdio   (used by AI Toolkit Agent Builder)
  http:  python mcp-server/server.py            (runs at http://127.0.0.1:8000/mcp)
"""

import argparse
import asyncio
import json
import os
from typing import Annotated

from mcp.server.fastmcp import FastMCP
from pydantic import Field

# ------------------------------------------------------------------
# Server initialisation
# ------------------------------------------------------------------
mcp = FastMCP("Biashara Agent Data Server")

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


def _load(filename: str) -> dict:
    """Load a JSON data file from the data directory."""
    with open(os.path.join(DATA_DIR, filename), "r", encoding="utf-8") as f:
        return json.load(f)


# ------------------------------------------------------------------
# Tool 1 — Business FAQs
# ------------------------------------------------------------------
@mcp.tool()
def search_business_faqs(
    query: Annotated[str, Field(description="The customer's question or keywords to search for.")],
) -> str:
    """Search Savanna Bites Restaurant FAQs.

    Use this tool to answer questions about:
    - Delivery areas and fees
    - How to place an order (walk-in, WhatsApp, delivery apps)
    - Payment methods (M-Pesa, cash, card)
    - Opening hours and meal times
    - Catering and event orders
    - Dietary options and allergies
    - Loyalty programme and reservations
    - Complaints and refunds
    - Contact details
    """
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


# ------------------------------------------------------------------
# Tool 2 — Product Catalogue
# ------------------------------------------------------------------
@mcp.tool()
def get_product_catalogue(
    category: Annotated[str, Field(
        description="Filter by category. Options: 'breakfast', 'lunch', 'snacks', 'drinks', or 'all' (default)."
    )] = "all",
) -> str:
    """Get the current menu and prices for Savanna Bites Restaurant.

    Use this tool to answer questions about:
    - What meals and snacks are available
    - Current prices (in KES)
    - Whether an item is in stock
    - Whether an item is seasonal
    - Meal descriptions and ingredients
    """
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


# ------------------------------------------------------------------
# Tool 3 — Daily Specials & Promotions
# ------------------------------------------------------------------
@mcp.tool()
def get_daily_specials(
    category: Annotated[str, Field(
        description="Filter by category. Options: 'specials', 'combos', 'promotions', or 'all' (default)."
    )] = "all",
) -> str:
    """Get today's daily specials, combo deals, and active promotions.

    Use this tool to answer questions about:
    - Today's special meal and its price
    - Lunch combo deals (e.g. Office Lunch, Snack Attack)
    - Weekly promotions and loyalty club offers
    - Group deals and catering discounts
    """
    data = _load("daily-specials.json")
    lines = [
        f"Daily Specials & Offers — {data['business']}",
        f"Note: {data['note']}",
        "=" * 50,
    ]

    cat_lower = category.lower()

    # 1. Daily Specials
    if cat_lower in ["all", "specials", "daily"]:
        lines.append("\n--- Weekly Daily Specials ---")
        for s in data["daily_specials"]:
            price_str = f"KES {s['special_price']}" if s["special_price"] else "See details"
            lines.append(
                f"  {s['day']} ({s['day_sw']}): {s['name_en']} / {s['name_sw']} — {price_str}"
            )
            lines.append(f"    {s['description']} (Available: {s['available']})")

    # 2. Combo Deals
    if cat_lower in ["all", "combos", "combo"]:
        lines.append("\n--- Combo Deals (Every Day) ---")
        for c in data["combo_deals"]:
            lines.append(
                f"  {c['name_en']} / {c['name_sw']}: KES {c['combo_price']} (Save KES {c['saving']})"
            )
            lines.append(f"    {c['description']} (Available: {c['available']})")

    # 3. Promotions
    if cat_lower in ["all", "promotions", "promo"]:
        lines.append("\n--- Active Promotions ---")
        for p in data["promotions"]:
            lines.append(f"  {p['name_en']} / {p['name_sw']}")
            lines.append(f"    {p['description']}")
            lines.append(f"    Validity: {p['valid_from']} to {p['valid_to']}")

    return "\n".join(lines)


# ------------------------------------------------------------------
# Entry point
# ------------------------------------------------------------------
def main() -> None:
    """Main entry point for the MCP server."""
    parser = argparse.ArgumentParser(description="Biashara Agent MCP Data Server")
    parser.add_argument(
        "--stdio",
        action="store_true",
        help="Run server in stdio mode (used by AI Toolkit Agent Builder)",
    )
    args = parser.parse_args()

    if args.stdio:
        print("Starting Biashara Agent MCP Data Server (stdio)...")
        print("Tools available: search_business_faqs, get_product_catalogue")
        mcp.run()
    else:
        print("Starting Biashara Agent MCP Data Server (HTTP)...")
        print(f"📡 MCP endpoint available at: http://127.0.0.1:8000/mcp")
        print("Tools available: search_business_faqs, get_product_catalogue")
        asyncio.run(mcp.run_streamable_http_async())


if __name__ == "__main__":
    main()
