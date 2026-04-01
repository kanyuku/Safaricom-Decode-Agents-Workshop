import json
import os

# Mock the directory structure
DATA_DIR = os.path.join(os.path.dirname(__file__), "mcp-server", "data")

def _load(filename):
    with open(os.path.join(DATA_DIR, filename), "r", encoding="utf-8") as f:
        return json.load(f)

def get_daily_specials(category="all"):
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
            price_str = f"KES {s['special_price']}" if s["special_price"] else "See details"
            lines.append(f"  {s['day']} ({s['day_sw']}): {s['name_en']} / {s['name_sw']} — {price_str}")
            lines.append(f"    {s['description']} (Available: {s['available']})")
    if cat_lower in ["all", "combos", "combo"]:
        lines.append("\n--- Combo Deals (Every Day) ---")
        for c in data["combo_deals"]:
            lines.append(f"  {c['name_en']} / {c['name_sw']}: KES {c['combo_price']} (Save KES {c['saving']})")
            lines.append(f"    {c['description']} (Available: {c['available']})")
    if cat_lower in ["all", "promotions", "promo"]:
        lines.append("\n--- Active Promotions ---")
        for p in data["promotions"]:
            lines.append(f"  {p['name_en']} / {p['name_sw']}")
            lines.append(f"    {p['description']}")
            lines.append(f"    Validity: {p['valid_from']} to {p['valid_to']}")
    return "\n".join(lines)

if __name__ == "__main__":
    print("Testing 'all' category:")
    print(get_daily_specials("all"))
    print("\n" + "#"*40 + "\n")
    print("Testing 'combos' category:")
    print(get_daily_specials("combos"))
