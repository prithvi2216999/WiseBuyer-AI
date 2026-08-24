from flask import Flask, request, jsonify, render_template
import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# -----------------------
# 🔑 GROQ API SETTINGS
# -----------------------
GROQ_API_KEY = os.getenv("GROQ_API_KEY")  # <<< PUT YOUR KEY HERE
GROQ_MODEL = "llama-3.1-8b-instant"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

# -----------------------
# 📂 LOAD LOCAL PRODUCT DB
# -----------------------
DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "products.json")
if os.path.exists(DATA_PATH):
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        PRODUCTS = json.load(f)
else:
    PRODUCTS = {}

CATEGORIES = list(PRODUCTS.keys())  # e.g. ["Mobile","Laptop","TV",...]

# Section menu options (buttons)
SECTION_OPTIONS = [
    "📘 Full Specs",
    "📊 Comparison",
    "🧠 AI Reasoning",
    "👥 Social Proof",
    "💬 Sentiment Analysis",
    "📈 Price & Resale Prediction",
    "✅ Final Recommendation",
    "💸 Financial Advisor",
    "🔄 New Product"
]

# -----------------------
# 🧠 CALL GROQ
# -----------------------
def ai(prompt: str) -> str:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROQ_API_KEY}",
    }

    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are WiseBuyer AI, a concise, clear buying assistant. "
                    "Use short bullet points and simple language. Avoid long paragraphs."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.4,
    }

    try:
        resp = requests.post(GROQ_URL, headers=headers, json=payload)
        data = resp.json()
        if "choices" in data and data["choices"]:
            return data["choices"][0]["message"]["content"]
        if "error" in data:
            return "⚠️ AI Error: " + data["error"].get("message", "Unknown error")
        return "⚠️ Unexpected AI response."
    except Exception as e:
        return f"⚠️ AI Exception: {e}"


# -----------------------
# 🔧 HELPERS: DB ACCESS
# -----------------------
def get_brands(category: str):
    return sorted(PRODUCTS.get(category, {}).keys())


def get_models(category: str, brand: str):
    brand_data = PRODUCTS.get(category, {}).get(brand, [])
    return [m["model"] for m in brand_data]


def find_product(category: str, brand: str, model_name: str):
    for m in PRODUCTS.get(category, {}).get(brand, []):
        if m["model"].lower() == model_name.lower():
            return m
    return None


def get_all_category_products(category: str):
    result = []
    cat = PRODUCTS.get(category, {})
    for brand, items in cat.items():
        for p in items:
            p_copy = p.copy()
            p_copy["brand"] = brand
            result.append(p_copy)
    return result


# -----------------------
# 📊 COMPARISON TABLE
# -----------------------
FEATURE_MAP = {
    "Mobile": [
        ("display", "Display"),
        ("battery", "Battery"),
        ("camera", "Camera"),
        ("processor", "Processor"),
        ("price", "Price")
    ],
    "Laptop": [
        ("display", "Display"),
        ("processor", "CPU"),
        ("ram", "RAM"),
        ("storage", "Storage"),
        ("price", "Price")
    ],
    "TV": [
        ("display", "Display"),
        ("size", "Size"),
        ("panel", "Panel"),
        ("os", "OS"),
        ("price", "Price")
    ],
    "Bike": [
        ("engine", "Engine"),
        ("mileage", "Mileage"),
        ("power", "Power"),
        ("abs", "ABS"),
        ("price", "Price")
    ],
    "Car": [
        ("engine", "Engine"),
        ("mileage", "Mileage"),
        ("safety", "Safety"),
        ("segment", "Segment"),
        ("price", "Price")
    ],
    "Refrigerator": [
        ("capacity", "Capacity"),
        ("type", "Type"),
        ("stars", "Star Rating"),
        ("inverter", "Inverter"),
        ("price", "Price")
    ],
    "AC": [
        ("capacity", "Capacity"),
        ("type", "Type"),
        ("stars", "Star Rating"),
        ("price", "Price")
    ],
    "Washing Machine": [
        ("capacity", "Capacity"),
        ("type", "Type"),
        ("stars", "Star Rating"),
        ("price", "Price")
    ]
}


def build_specs_summary(category: str, product: dict) -> str:
    lines = []
    lines.append(f"📘 Full Specs for {product.get('brand', '')} {product['model']}")
    lines.append("")
    lines.append("🔹 Key Specs:")

    for key in [
        "display", "processor", "ram", "storage",
        "battery", "camera", "engine", "mileage",
        "capacity", "type", "size", "panel", "stars"
    ]:
        if key in product:
            label = key.replace("_", " ").title()
            lines.append(f"- {label}: {product[key]}")

    lines.append(f"- Segment: {product.get('segment', 'N/A')}")
    lines.append(f"- Approx Price: ₹{product['price']:,}")

    if "pros" in product:
        lines.append("")
        lines.append("✅ Pros:")
        for p in product["pros"]:
            lines.append(f"- {p}")

    if "cons" in product:
        lines.append("")
        lines.append("⚠️ Cons:")
        for c in product["cons"]:
            lines.append(f"- {c}")

    return "\n".join(lines)


def build_comparison(category: str, main_product: dict) -> str:
    all_products = get_all_category_products(category)
    # all other products in same category
    others = [
        p for p in all_products
        if p["model"].lower() != main_product["model"].lower()
    ]

    if not others:
        return "📊 Not enough products in this category to compare."

    # sort closest by price and take up to 4 competitors
    others_sorted = sorted(
        others, key=lambda x: abs(x["price"] - main_product["price"])
    )
    competitors = others_sorted[:4]   # ← main + 4 = up to 5 columns total

    feat_list = FEATURE_MAP.get(category, [("price", "Price")])

    headers = ["Feature", main_product["model"]] + [c["model"] for c in competitors]
    rows = []

    for key, label in feat_list:
        row = [label]
        vals = [main_product.get(key, "-")] + [c.get(key, "-") for c in competitors]
        row.extend(vals)
        rows.append(row)

    col_count = len(headers)
    out_lines = []
    out_lines.append(
        f"📊 Comparison for  {main_product.get('brand','')} {main_product['model']}:\n"
    )
    out_lines.append("| " + " | ".join(headers) + " |")
    out_lines.append("|" + " --- |" * col_count)

    for r in rows:
        out_lines.append("| " + " | ".join(str(x) for x in r) + " |")

    return "\n".join(out_lines)

# -----------------------
# 🧠 ADVANCED AI SECTIONS
# -----------------------
def build_reasoning_block(category: str, product: dict) -> str:
    prompt = f"""
You are WiseBuyer AI.

Product: {product.get('brand','')} {product['model']}
Category: {category}
Price: ₹{product['price']}
Segment: {product.get('segment','N/A')}

Give a short AI reasoning analysis in this structure:

🧠 Overall Verdict:
- 2 short bullets

⚙️ Performance & Usage:
- 2 bullets (how it performs in real life)

📈 Value for Money:
- 2 bullets (is price justified compared to rivals)

🛡️ Future Proofing:
- 2 bullets (how long it will stay good, software/tech life)

Use simple language. Keep each bullet short.
"""
    return ai(prompt)


def build_social_block(category: str, product: dict) -> str:
    prompt = f"""
You are WiseBuyer AI.

Imagine real user reviews & long-term owners of:
{product.get('brand','')} {product['model']} ({category}), price ₹{product['price']}.

Write:

👥 Social Proof & User Experience:
- 3 bullets (what people usually like)
- 2 bullets (common complaints)

🎯 Best For:
- 3 bullets (type of user/lifestyle)

🚫 Not Ideal For:
- 2 bullets (who should avoid this)

Be realistic but concise.
"""
    return ai(prompt)


def build_sentiment_block(category: str, product: dict) -> str:
    prompt = f"""
You are WiseBuyer AI.

For product: {product.get('brand','')} {product['model']} in {category}, price ₹{product['price']}.

Create a FAKE BUT PLAUSIBLE sentiment dashboard:

💬 Market Sentiment (approx):
- Positive: xx%
- Neutral: xx%
- Negative: xx%

🔥 Top 3 things people praise:
- ...

⚠️ Top 3 issues/concerns:
- ...

Keep it short and clean. No long explanation.
"""
    return ai(prompt)


def build_prediction_block(category: str, product: dict) -> str:
    prompt = f"""
You are WiseBuyer AI.

Product: {product.get('brand','')} {product['model']}
Category: {category}
Price now: ₹{product['price']}

Give a short prediction:

📈 Price Trend (Next 12 months):
- Month 0 price
- Month 6 expected price
- Month 12 expected price
- % possible savings if user waits

💰 Resale Value (3 years later):
- Expected resale price
- % value retained

⏳ Best Time to Buy:
- Simple suggestion: buy now / wait 3-6 months

Keep it in clear bullet points. No big story.
"""
    return ai(prompt)


def build_recommendation_block(category: str, product: dict) -> str:
    prompt = f"""
You are WiseBuyer AI, making a final buying recommendation.

Product: {product.get('brand','')} {product['model']}
Category: {category}
Price: ₹{product['price']}
Segment: {product.get('segment','N/A')}

Return:

✅ Final Recommendation:
- 2 bullets (overall verdict)

👍 You should buy this if:
- 3 bullets

🤔 You should look at other options if:
- 3 bullets

📌 One Alternative Suggestion:
- Name a typical alternative type (e.g., 'cheaper midrange from Samsung', not exact model)
- Explain in 1 line why.

Make everything short, clear, and practical.
"""
    return ai(prompt)


def build_financial_advice(product: dict, income: int, expense: int) -> str:
    prompt = f"""
You are a strict but friendly financial advisor in India.

Product: {product.get('brand','')} {product['model']}
Price: ₹{product['price']}
User Monthly Income: ₹{income}
User Monthly Expenses: ₹{expense}

Calculate roughly:
- Savings per month (income - expenses)
- If they buy with 12-month EMI at ~12% interest:
  - Approx EMI amount
  - How much savings will drop
- Risk level: Low / Medium / High (for their situation)

Return in this exact structure:

💰 Monthly Situation:
- ...

📉 EMI Impact:
- ...

🧠 Advisor Opinion:
- ...

🎯 Final Suggestion:
- ...

Be simple and realistic. No formulas, only final points.
"""
    return ai(prompt)


# -----------------------
# 🧠 SIMPLE SESSION STATE
# -----------------------
session = {
    "step": "start",
    "category": None,
    "brand": None,
    "model": None,
    "product": None,
    "income": None,
}


# -----------------------
# 🌐 ROUTES
# -----------------------
@app.route("/")
def index():
    session["step"] = "start"
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message", "").strip()
    step = session["step"]

    # 0️⃣ Auto start
    if user_msg == "__start__" or step == "start":
        session["step"] = "choose_category"
        return jsonify({
            "reply": "👋 Hi! I'm WiseBuyer AI.\nWhat category do you want to explore?",
            "options": CATEGORIES
        })

    # 1️⃣ Choose category
    if step == "choose_category":
        if user_msg not in CATEGORIES:
            return jsonify({
                "reply": "Please choose a category from above:",
                "options": CATEGORIES
            })

        session["category"] = user_msg
        brands = get_brands(user_msg)
        session["step"] = "choose_brand"

        return jsonify({
            "reply": f"Great! You chose **{user_msg}**.\nNow select a brand:",
            "options": brands
        })

    # 2️⃣ Choose brand
    if step == "choose_brand":
        category = session["category"]
        brands = get_brands(category)

        if user_msg not in brands:
            return jsonify({
                "reply": "Please select a brand from the list:",
                "options": brands
            })

        session["brand"] = user_msg
        models = get_models(category, user_msg)
        session["step"] = "choose_model"

        return jsonify({
            "reply": f"Nice! Now choose a model from **{user_msg}**:",
            "options": models
        })

    # 3️⃣ Choose model
    if step == "choose_model":
        category = session["category"]
        brand = session["brand"]
        models = get_models(category, brand)

        if user_msg not in models:
            return jsonify({
                "reply": "Please choose a model from the list:",
                "options": models
            })

        session["model"] = user_msg
        product = find_product(category, brand, user_msg)
        session["product"] = product

        # Short intro + show menu
        intro = (
            f"✅ You selected: {brand} {user_msg} in {category}.\n\n"
            "What would you like to see about this product?"
        )

        session["step"] = "section_menu"

        return jsonify({
            "reply": intro,
            "options": SECTION_OPTIONS
        })

    # 4️⃣ Section menu (user-controlled)
    if step == "section_menu":
        category = session["category"]
        product = session["product"]

        text = user_msg.lower()

        # New product reset
        if "new product" in text or "🔄" in user_msg:
            session["step"] = "choose_category"
            return jsonify({
                "reply": "Alright, let's start fresh. Choose a category:",
                "options": CATEGORIES
            })

        # Financial advisor → go to income step
        if "financial" in text or "advisor" in text or "💸" in user_msg:
            session["step"] = "income"
            return jsonify({
                "reply": "Okay! Let's check if this fits your budget.\nEnter your monthly income (₹):",
                "options": []
            })

        # Specs
        if "spec" in text:
            content = build_specs_summary(category, product)
            return jsonify({
                "reply": content + "\n\nYou can select another section:",
                "options": SECTION_OPTIONS
            })

        # Comparison
        if "comparison" in text or "compare" in text or "📊" in user_msg:
            content = build_comparison(category, product)
            return jsonify({
                "reply": content + "\n\nYou can select another section:",
                "options": SECTION_OPTIONS
            })

        # AI Reasoning
        if "reason" in text or "🧠" in user_msg:
            content = build_reasoning_block(category, product)
            return jsonify({
                "reply": content + "\n\nYou can select another section:",
                "options": SECTION_OPTIONS
            })

        # Social Proof
        if "social" in text or "proof" in text or "👥" in user_msg:
            content = build_social_block(category, product)
            return jsonify({
                "reply": content + "\n\nYou can select another section:",
                "options": SECTION_OPTIONS
            })

        # Sentiment
        if "sentiment" in text or "market" in text or "💬" in user_msg:
            content = build_sentiment_block(category, product)
            return jsonify({
                "reply": content + "\n\nYou can select another section:",
                "options": SECTION_OPTIONS
            })

        # Prediction
        if "price" in text or "prediction" in text or "resale" in text or "📈" in user_msg:
            content = build_prediction_block(category, product)
            return jsonify({
                "reply": content + "\n\nYou can select another section:",
                "options": SECTION_OPTIONS
            })

        # Final Recommendation
        if "final" in text or "recommend" in text or "✅" in user_msg:
            content = build_recommendation_block(category, product)
            return jsonify({
                "reply": content + "\n\nYou can still explore other sections or pick a new product.",
                "options": SECTION_OPTIONS
            })

        # If unrecognised - show menu again
        return jsonify({
            "reply": "Please choose one of the sections below:",
            "options": SECTION_OPTIONS
        })

    # 5️⃣ Get income
    if step == "income":
        if not user_msg.isdigit():
            return jsonify({
                "reply": "Please enter income in numbers only (no commas).",
                "options": []
            })
        session["income"] = int(user_msg)
        session["step"] = "expense"
        return jsonify({
            "reply": "Now enter your monthly expenses (₹):",
            "options": []
        })

    # 6️⃣ Get expenses & show financial advice
    if step == "expense":
        if not user_msg.isdigit():
            return jsonify({
                "reply": "Please enter expenses in numbers only (no commas).",
                "options": []
            })

        expense = int(user_msg)
        income = session["income"]
        product = session["product"]

        fin_text = build_financial_advice(product, income, expense)

        session["step"] = "section_menu"

        return jsonify({
            "reply": (
                f"💸 Personalised Financial Advisor for "
                f"{product.get('brand','')} {product['model']}:\n\n"
                f"{fin_text}\n\nYou can choose another section:"
            ),
            "options": SECTION_OPTIONS
        })

    # fallback
    session["step"] = "choose_category"
    return jsonify({
        "reply": "Let's start over. Choose a category:",
        "options": CATEGORIES
    })


# -----------------------
# RUN SERVER
# -----------------------
if __name__ == "__main__":
    import webbrowser, threading
    threading.Timer(1, lambda: webbrowser.open("http://127.0.0.1:5000")).start()
    app.run(debug=True)
