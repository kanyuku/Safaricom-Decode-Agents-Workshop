const express = require('express');
const { OpenAI } = require('openai');
const fs = require('fs');
const path = require('path');
const cors = require('cors');
require('dotenv').config();

const app = express();
const port = process.env.PORT || 5000;

app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, 'templates')));

// --------------- Configuration ---------------
const GITHUB_TOKEN = process.env.GITHUB_TOKEN || "";
const MODEL = process.env.MODEL || "gpt-4.1-mini";
const ENDPOINT = process.env.ENDPOINT || "https://models.github.ai/inference";

const DATA_DIR = path.join(__dirname, "..", "mcp-server", "data");

const SYSTEM_PROMPT = `
You are Biashara Agent, an intelligent and friendly AI assistant for Savanna Bites Restaurant in Nairobi CBD. You help customers with their dining needs by understanding what they are looking for and recommending the most suitable items from the menu.

Your role is to:
- Engage with the customer in natural conversation to understand what they need.
- Ask thoughtful questions to gather relevant details.
- Be brief in your responses.
- Provide the best solution for the customer's question and only recommend items within Savanna Bites' menu.
- Search the restaurant's product catalogue to identify items that best match the customer's needs.
- Clearly explain what each recommended item is, why it's a good fit, and how much it costs.
- Reply in the user's language (English, Swahili, or mixed/Sheng).

Your personality is:
- Warm and welcoming, like a friendly waiter
- Professional and knowledgeable, like a seasoned restaurant host
- Curious and conversational — never assume, always clarify
- Transparent and honest — if something isn't available, offer support anyway

If no matching items are found in the catalogue, say:
"Thanks for sharing those details! I've searched our menu, but it looks like we don't currently have something that fits your exact request. If you'd like, I can suggest some alternatives or help you find something similar."

## Safety guardrails
- Only discuss topics related to Savanna Bites Restaurant: menu items, prices, delivery, catering, and restaurant information.
- Do not generate, link to, or discuss content that is harmful, hateful, or illegal.
`;

// --------------- Data helpers ---------------

function loadData(filename) {
    const filePath = path.join(DATA_DIR, filename);
    return JSON.parse(fs.readFileSync(filePath, 'utf8'));
}

function searchBusinessFaqs(query) {
    const data = loadData('business-faqs.json');
    const queryWords = query.toLowerCase().split(/\s+/);
    const matches = [];

    data.faqs.forEach(faq => {
        const searchable = [
            faq.question,
            faq.answer,
            faq.question_sw,
            faq.answer_sw,
            ...(faq.keywords || [])
        ].join(" ").toLowerCase();

        if (queryWords.some(word => searchable.includes(word))) {
            matches.push(`**Q: ${faq.question}**\nA: ${faq.answer}\n\n*(Kwa Kiswahili)* ${faq.answer_sw || ''}`);
        }
    });

    if (matches.length === 0) {
        return "Hakuna majibu yaliyopatikana kwa swali hilo.\nNo FAQs matched your query. Try keywords like: delivery, payment, order, menu, contact, hours.";
    }

    const business = data.business;
    const header = `Business: ${business.name}\nPhone/WhatsApp: ${business.phone} | M-Pesa Paybill: ${business.mpesa_paybill} (Acc: ${business.mpesa_account})\nHours: ${business.hours.weekdays} | ${business.hours.sunday}\n--------------------------------------------------\n`;
    return header + matches.join("\n\n");
}

function getProductCatalogue(category = "all") {
    const data = loadData('product-catalogue.json');
    let lines = [
        `Product Catalogue — ${data.business}`,
        `Updated: ${data.last_updated} | Currency: ${data.currency}`,
        `Note: ${data.note}`,
        "=".repeat(50)
    ];

    data.categories.forEach(cat => {
        if (category === "all" || cat.name.toLowerCase().includes(category.toLowerCase())) {
            lines.push(`\n--- ${cat.name} (${cat.name_sw}) ---`);
            cat.products.forEach(p => {
                const stock = p.in_stock ? "✓ In stock" : "✗ Out of stock";
                const seasonal = p.seasonal ? " [Seasonal]" : "";
                lines.push(`  ${p.name_en} / ${p.name_sw}: KES ${p.price} per ${p.unit} — ${stock}${seasonal}`);
                lines.push(`    Origin: ${p.origin || 'N/A'} | ${p.description}`);
            });
        }
    });

    if (lines.length <= 4) {
        const available = data.categories.map(c => c.name.toLowerCase()).join(", ");
        return `Category '${category}' not found.\nAvailable categories: ${available}, or 'all'.`;
    }

    return lines.join("\n");
}

function getDailySpecials(category = "all") {
    const data = loadData('daily-specials.json');
    let lines = [
        `Daily Specials & Offers — ${data.business}`,
        `Note: ${data.note}`,
        "=".repeat(50)
    ];

    const catLower = category.toLowerCase();

    if (["all", "specials", "daily"].includes(catLower)) {
        lines.push("\n--- Weekly Daily Specials ---");
        data.daily_specials.forEach(s => {
            const priceStr = s.special_price ? `KES ${s.special_price}` : "See details";
            lines.push(`  ${s.day} (${s.day_sw}): ${s.name_en} / ${s.name_sw} — ${priceStr}`);
            lines.push(`    ${s.description} (Available: ${s.available})`);
        });
    }

    if (["all", "combos", "combo"].includes(catLower)) {
        lines.push("\n--- Combo Deals (Every Day) ---");
        data.combo_deals.forEach(c => {
            lines.push(`  ${c.name_en} / ${c.name_sw}: KES ${c.combo_price} (Save KES ${c.saving})`);
            lines.push(`    ${c.description} (Available: ${c.available})`);
        });
    }

    if (["all", "promotions", "promo"].includes(catLower)) {
        lines.push("\n--- Active Promotions ---");
        data.promotions.forEach(p => {
            lines.push(`  ${p.name_en} / ${p.name_sw}`);
            lines.push(`    ${p.description}`);
            lines.push(`    Validity: ${p.valid_from} to ${p.valid_to}`);
        });
    }

    return lines.join("\n");
}

// --------------- OpenAI tool definitions ---------------

const TOOLS = [
    {
        type: "function",
        function: {
            name: "search_business_faqs",
            description: "Search Savanna Bites Restaurant FAQs. Use this to find info on delivery, payment, ordering, hours, etc.",
            parameters: {
                type: "object",
                properties: {
                    query: { type: "string", description: "Keywords to search for." }
                },
                required: ["query"]
            }
        }
    },
    {
        type: "function",
        function: {
            name: "get_product_catalogue",
            description: "Get the current menu and prices. Options: 'breakfast', 'lunch', 'snacks', 'drinks', or 'all'.",
            parameters: {
                type: "object",
                properties: {
                    category: { type: "string", default: "all" }
                }
            }
        }
    },
    {
        type: "function",
        function: {
            name: "get_daily_specials",
            description: "Get today's daily specials, combo deals, and active promotions.",
            parameters: {
                type: "object",
                properties: {
                    category: { type: "string", default: "all", enum: ["specials", "combos", "promotions", "all"] }
                }
            }
        }
    }
];

const TOOL_FUNCTIONS = {
    search_business_faqs: searchBusinessFaqs,
    get_product_catalogue: getProductCatalogue,
    get_daily_specials: getDailySpecials
};

// --------------- In-memory conversation store ---------------
const conversations = {};

// --------------- Routes ---------------

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'templates', 'index.html'));
});

app.post('/api/chat', async (req, res) => {
    const { message, session_id } = req.body;
    if (!message) return res.status(400).json({ error: "Missing message" });

    const sid = session_id || require('crypto').randomUUID();
    if (!conversations[sid]) {
        conversations[sid] = [{ role: "system", content: SYSTEM_PROMPT }];
    }

    conversations[sid].push({ role: "user", content: message.trim() });

    if (!GITHUB_TOKEN) {
        return res.json({ response: "⚠️ GITHUB_TOKEN is not set. Please set it in your environment or .env file to chat.", session_id: sid });
    }

    const client = new OpenAI({ baseURL: ENDPOINT, apiKey: GITHUB_TOKEN });

    try {
        let currentRole = "assistant";
        let lastResponse = null;

        for (let round = 0; round < 5; round++) {
            const response = await client.chat.completions.create({
                model: MODEL,
                messages: conversations[sid],
                tools: TOOLS
            });

            const assistantMsg = response.choices[0].message;
            conversations[sid].push(assistantMsg);
            lastResponse = assistantMsg;

            if (!assistantMsg.tool_calls || assistantMsg.tool_calls.length === 0) break;

            for (const toolCall of assistantMsg.tool_calls) {
                const fnName = toolCall.function.name;
                const fn = TOOL_FUNCTIONS[fnName];
                const args = JSON.parse(toolCall.function.arguments);
                const result = fn ? fn(args.query || args.category) : `Unknown tool: ${fnName}`;

                conversations[sid].push({
                    role: "tool",
                    tool_call_id: toolCall.id,
                    content: result
                });
            }
        }

        res.json({ response: lastResponse.content || "", session_id: sid });

    } catch (err) {
        console.error(err);
        res.status(500).json({ error: "AI Inference failed. Check your API key and connection." });
    }
});

app.post('/api/reset', (req, res) => {
    const { session_id } = req.body;
    if (session_id && conversations[session_id]) delete conversations[session_id];
    res.json({ status: "ok" });
});

app.listen(port, () => {
    console.log(`\n🍽️  Biashara Agent (Node.js) starting...`);
    console.log(`   Model: ${MODEL}`);
    console.log(`   Endpoint: ${ENDPOINT}`);
    console.log(`   Open http://127.0.0.1:${port} in your browser\n`);
});
