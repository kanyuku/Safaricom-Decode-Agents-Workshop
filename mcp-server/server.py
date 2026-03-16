"""
Mama Mboga Fresh Supplies — Biashara Bot MCP Data Server
=========================================================
A FastMCP server that exposes business data for the Biashara Bot AI agent.
Participants: you do NOT need to edit this file during the workshop.
Just run it, then configure your AI Toolkit agent to use it.

Run: python mcp-server/server.py
"""

import json
import os
from mcp.server.fastmcp import FastMCP

# ------------------------------------------------------------------
# Server initialisation
# ------------------------------------------------------------------
mcp = FastMCP("Biashara Bot Data Server")

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


def _load(filename: str) -> dict:
    """Load a JSON data file from the data directory."""
    with open(os.path.join(DATA_DIR, filename), "r", encoding="utf-8") as f:
        return json.load(f)


# ------------------------------------------------------------------
# Tool 1 — Business FAQs
# ------------------------------------------------------------------
@mcp.tool()
def search_business_faqs(query: str) -> str:
    """
    Search Mama Mboga Fresh Supplies FAQs.

    Use this tool to answer questions about:
    - Delivery areas and fees
    - How to place an order
    - Payment methods (M-Pesa, cash)
    - Business hours
    - Freshness guarantee and returns
    - Wholesale and subscription options
    - Contact details

    Args:
        query: The customer's question or keywords to search for.

    Returns:
        Matching FAQ entries in English and Swahili, or a not-found message.
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
            "delivery, payment, order, wholesale, fresh, contact, hours."
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
def get_product_catalogue(category: str = "all") -> str:
    """
    Get the current product catalogue and retail prices for Mama Mboga Fresh Supplies.

    Use this tool to answer questions about:
    - What produce is available today
    - Current retail prices (in KES)
    - Whether a product is in stock
    - Whether a product is seasonal
    - Where the produce comes from (farm origin)

    Args:
        category: Filter by category. Options: "vegetables", "leafy vegetables",
                  "fruits", "herbs", or "all" (default).

    Returns:
        A formatted list of products with names (English & Swahili), prices, and stock status.
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
# Tool 3 — Nairobi Wholesale Market Prices
# ------------------------------------------------------------------
@mcp.tool()
def get_market_prices(produce_name: str = "all") -> str:
    """
    Get current Nairobi wholesale market reference prices from Wakulima and Gikomba markets.

    Use this tool to:
    - Help customers understand general market price context
    - Compare Mama Mboga's retail prices against wholesale benchmarks
    - Explain seasonal price trends (rising, falling, stable)

    Args:
        produce_name: Name of the produce to look up (English or Swahili),
                      or "all" to return everything.

    Returns:
        Wholesale price data with trend indicators and market analyst notes.
    """
    data = _load("market-prices.json")
    prices = data["prices"]

    if produce_name != "all":
        prices = [
            p for p in prices
            if produce_name.lower() in p["name_en"].lower()
            or produce_name.lower() in p["name_sw"].lower()
        ]

    if not prices:
        names = [p["name_en"] for p in data["prices"]]
        return (
            f"No market price data found for '{produce_name}'.\n"
            f"Available items: {', '.join(names)}"
        )

    trend_icon = {"rising": "↑", "falling": "↓", "stable": "→"}

    lines = [
        f"Nairobi Wholesale Market Prices ({data['date']})",
        f"Source: {', '.join(m['name'] for m in data['markets'])}",
        f"Note: {data['note']}",
        "=" * 50,
    ]

    for p in prices:
        icon = trend_icon.get(p.get("trend", "stable"), "→")
        lines.append(
            f"\n{p['name_en']} / {p['name_sw']} [{p['market']}]"
            f"\n  Wholesale: KES {p['wholesale_price']} per {p['unit']}"
            f"\n  Trend: {icon} {p.get('trend', 'stable').upper()}"
            f"\n  Notes: {p.get('notes', '')}"
        )

    lines.append(f"\n{'=' * 50}")
    lines.append(f"Analyst Overview: {data['analyst_notes']}")
    return "\n".join(lines)


# ------------------------------------------------------------------
# Tool 4 — Kenya Tax & Business Compliance Info
# ------------------------------------------------------------------
@mcp.tool()
def get_tax_info(topic: str = "all") -> str:
    """
    Get Kenya tax and business compliance information for small businesses (MSMEs).

    Use this tool for general educational information about:
    - KRA PIN registration
    - iTax portal and filing returns
    - VAT (threshold: KES 5 million, fresh produce is exempt)
    - Income tax bands and Turnover Tax (3% option)
    - PAYE for employers
    - Business registration via eCitizen / BRS
    - Hustler Fund loans
    - SACCOs
    - County business permit (Single Business Permit)

    IMPORTANT: Always remind the customer that this is general information only
    and they should consult a certified accountant or KRA directly for
    advice specific to their situation.

    Args:
        topic: Specific topic to look up (e.g., "VAT", "Hustler Fund", "PAYE",
               "business registration", "SACCO"), or "all" for everything.

    Returns:
        Relevant tax/compliance information with a disclaimer.
    """
    data = _load("kenyan-tax.json")
    sections = data["sections"]

    disclaimer = (
        "\n⚠️  DISCLAIMER: This is general information only. "
        "For advice specific to your business, consult a certified accountant "
        "or contact KRA directly at itax.kra.go.ke or 0800 720 1000 (toll-free)."
    )

    if topic == "all":
        lines = [
            "Kenya Business & Tax Reference — Mama Mboga Bot",
            f"Last reviewed: {data['last_reviewed']}",
            f"Note: {data['note']}",
            "=" * 50,
        ]
        for section in sections:
            lines.append(f"\n=== {section['title']} ===")
            lines.append(section["summary"])
        lines.append(disclaimer)
        return "\n".join(lines)

    # Search sections by title or keywords
    topic_lower = topic.lower()
    results = [
        s for s in sections
        if topic_lower in s["title"].lower()
        or any(topic_lower in kw.lower() for kw in s.get("keywords", []))
    ]

    if not results:
        available = [s["title"] for s in sections]
        return (
            f"No tax info found for '{topic}'.\n"
            f"Available topics: {', '.join(available)}"
        )

    lines = []
    for s in results:
        lines.append(f"=== {s['title']} ===\n{s['summary']}")
    lines.append(disclaimer)
    return "\n\n".join(lines)


# ------------------------------------------------------------------
# Entry point
# ------------------------------------------------------------------
if __name__ == "__main__":
    print("Starting Biashara Bot MCP Data Server...")
    print("Transport: stdio (AI Toolkit will connect automatically)")
    print("Tools available: search_business_faqs, get_product_catalogue,")
    print("                 get_market_prices, get_tax_info")
    mcp.run()
