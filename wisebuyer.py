# wisebuyer.py
# Core logic for WiseBuyer AI - Advanced Smart Purchase Advisor

class FinancialAdvisor:
    def analyze(self, product_name, price, user_finance):
        income = user_finance.get("monthly_income", 0)
        expenses = user_finance.get("monthly_expenses", 0)

        savings = income - expenses
        emi_12 = price / 12 if price else 0

        before_rate = (savings / income * 100) if income else 0
        after_savings = savings - emi_12
        after_rate = (after_savings / income * 100) if income else 0

        text = f"""
💸 FINANCIAL ANALYSIS: {product_name}

Monthly income: ₹{income:,.0f}
Monthly expenses: ₹{expenses:,.0f}
Current monthly savings: ₹{savings:,.0f}

If you buy on 12-month EMI:
• EMI amount: ₹{emi_12:,.0f} / month

Savings rate:
• Before EMI: {before_rate:.1f}%
• After EMI:  {after_rate:.1f}%
"""

        if after_rate < 5:
            rec = "🚨 Very risky. Your savings will almost disappear. Avoid or delay this purchase."
        elif after_rate < 10:
            rec = "⚠️ Tight situation. Buy only if this product is extremely important."
        else:
            rec = "✅ Financially acceptable. You can manage this EMI reasonably well."

        return text + "\n" + rec


class SocialProofAggregator:
    def summarize(self, product_name):
        # For project: we simulate realistic stats
        text = f"""
👥 SOCIAL EXPERIENCE: {product_name}

User satisfaction (approximate):
• After 1 month: 92% happy
• After 3 months: 85% happy
• After 6 months: 78% happy

Common Complaints:
1. Battery life drops slightly after some months
2. Heating during heavy gaming / camera usage
3. Occasional small software bugs

Top Praises:
1. Overall performance feels smooth in daily use
2. Display and design are highly appreciated
3. Brand trust and ecosystem value are strong
"""
        return text


class PricePredictor:
    def predict(self, product_name, current_price, months=6):
        prices = []
        price = current_price

        for m in range(months + 1):
            if m == 0:
                reason = "Launch / current price"
            elif m == 2:
                reason = "Festival / seasonal discounts"
            elif m == 4:
                reason = "New competitor / next model coming"
            else:
                reason = "Normal market depreciation"

            prices.append((m, round(price), reason))

            if m in (2, 4):
                price *= 0.95  # bigger drop
            else:
                price *= 0.98  # small drop

        best_month, best_price, _ = min(prices, key=lambda x: x[1])

        lines = [f"📈 PRICE FORECAST: {product_name}",
                 f"Current Price: ₹{current_price:,.0f}\n",
                 "Month | Predicted Price | Reason",
                 "-" * 45]

        for m, p, r in prices:
            label = "Now" if m == 0 else f"+{m} month(s)"
            lines.append(f"{label:<8} | ₹{p:<11,} | {r}")

        when = "Now" if best_month == 0 else f"in {best_month} month(s)"
        lines.append(f"\n💰 Best time to buy: {when} @ approx ₹{best_price:,.0f}")

        return "\n".join(lines)


class BargainingAssistant:
    def strategy(self, product_name, mrp, online_price=None):
        estimated_margin = mrp * 0.12  # assume ~12% dealer margin
        target_price = mrp - estimated_margin * 0.6

        if online_price and online_price < target_price:
            target_price = online_price - 1000

        text = f"""
💼 BARGAINING GUIDE: {product_name}

MRP: ₹{mrp:,.0f}
Estimated dealer margin: ~₹{estimated_margin:,.0f}

🎯 Target in store:
Try closing around: ₹{target_price:,.0f}

Suggested dialogue:
1. "Online I saw near ₹{target_price+3000:,.0f}, can you match that with GST bill?"
2. "Can you include a free case and screen guard?"
3. Stay polite but firm.

❌ Avoid:
• Useless add-ons (extra insurance without clear benefit)
• Overpriced accessories

✅ Must:
• Check seal pack and IMEI/serial in invoice
"""
        return text


class ScenarioSimulator:
    def simulate(self, product_name):
        text = f"""
🎭 FUTURE SCENARIOS: {product_name}

Best Case (30% chance):
• You love using it daily
• No major issues for 2–3 years
• You feel it was totally worth the money

Worst Case (15% chance):
• New version launches soon with better value
• A common issue appears (battery, heating)
• You face a financial emergency soon after buying

Most Likely (55% chance):
• You are happy overall
• Small price drops later (normal)
• Works fine for a few years, then you plan upgrade

⭐ Interpretation:
If your money situation is stable and you really need this,
risk is moderate. If money is tight or this is pure luxury,
waiting can reduce regret.
"""
        return text


class CommunityAnalyzer:
    def analyze(self, product_name, brand_name):
        text = f"""
👥 COMMUNITY & SUPPORT: {product_name} ({brand_name})

Service & Support:
• Good support in big cities, mixed in smaller towns
• Typical repair time: about 3–7 days
• Common parts usually available, special parts may take longer

Community:
• Many online forums and YouTube videos with tips and fixes
• Active user groups share real-life experiences
• Easier to find solutions for popular models

Meaning:
• Popular product = easier to get help, advice and spare parts.
• Rare product = more unique, but support may be slower.
"""
        return text


class SentimentDashboard:
    def get_sentiment(self, product_name):
        text = f"""
📊 MARKET SENTIMENT: {product_name}

Overall tech community mood:
• Positive: around 40–50%
• Neutral: around 30–40%
• Negative: around 15–25%

Positive themes:
• Performance feels smooth
• People like design and feel
• Features are enough for daily use

Negative themes:
• Some feel price is slightly high
• A few heating / battery complaints
• Strong competition in the same price range

Summary:
People mostly like this product, but it is not perfect.
There are some trade-offs you should be aware of.
"""
        return text


class WiseBuyerAI:
    def __init__(self):
        self.financial = FinancialAdvisor()
        self.social = SocialProofAggregator()
        self.price = PricePredictor()
        self.bargain = BargainingAssistant()
        self.scenario = ScenarioSimulator()
        self.community = CommunityAnalyzer()
        self.sentiment = SentimentDashboard()

    def build_report(self, product_name, brand_name, price, user_finance, online_price=None):
        sections = []

        sections.append(self.financial.analyze(product_name, price, user_finance))
        sections.append(self.social.summarize(product_name))
        sections.append(self.price.predict(product_name, price))
        sections.append(self.bargain.strategy(product_name, price, online_price))
        sections.append(self.scenario.simulate(product_name))
        sections.append(self.community.analyze(product_name, brand_name))
        sections.append(self.sentiment.get_sentiment(product_name))

        full_report = "\n" + "=" * 70 + "\n\n".join(sections)
        return full_report
