from models.sentiment_analysis import analyze_sentiment
from models.risk_assessment import calculate_risk_score
import numpy as np  # ensure this is imported



# Dummy financial offers (normally this comes from DB or partner APIs)
FINANCIAL_PRODUCTS = [
    {
        "title": "Platinum Rewards Card",
        "description": "Premium credit card with lounge access & reward points.",
        "min_income": 80000,
        "max_risk": 60,
        "min_sentiment": 0.7,
        "type": "Credit Card"
    },
    {
        "title": "Smart Saver Investment Plan",
        "description": "Low-risk investment plan with decent returns.",
        "min_income": 40000,
        "max_risk": 90,
        "min_sentiment": 0.5,
        "type": "Investment"
    },
    {
        "title": "Startup Booster Loan",
        "description": "Flexible small business loan for entrepreneurs.",
        "min_income": 50000,
        "max_risk": 50,
        "min_sentiment": 0.6,
        "type": "Loan"
    },
    {
        "title": "Digital Wallet Bonus Plan",
        "description": "Instant cashback and reward vouchers on signup.",
        "min_income": 30000,
        "max_risk": 100,
        "min_sentiment": 0.3,
        "type": "Utility"
    },
    {
        "title": "Youth Savings Account",
        "description": "Zero balance account with digital perks for youth.",
        "min_income": 0,
        "max_risk": 95,
        "min_sentiment": 0.2,
        "type": "Savings"
    },
    {
        "title": "Premium Travel Card",
        "description": "Frequent flyer card for international travel rewards.",
        "min_income": 100000,
        "max_risk": 40,
        "min_sentiment": 0.75,
        "type": "Credit Card"
    },
    {
        "title": "Lifestyle EMI Card",
        "description": "Convert lifestyle purchases into 0% EMI payments.",
        "min_income": 60000,
        "max_risk": 70,
        "min_sentiment": 0.5,
        "type": "Utility"
    },
    {
        "title": "Tech Investor Plan",
        "description": "Equity-based investment targeting tech sector.",
        "min_income": 75000,
        "max_risk": 50,
        "min_sentiment": 0.7,
        "type": "Investment"
    },
    {
        "title": "Gold-Backed Loan",
        "description": "Low-interest personal loan against gold.",
        "min_income": 40000,
        "max_risk": 85,
        "min_sentiment": 0.4,
        "type": "Loan"
    },
    {
        "title": "Freelancer Cashflow Loan",
        "description": "Quick-access loan for freelancers with cash flow needs.",
        "min_income": 30000,
        "max_risk": 65,
        "min_sentiment": 0.6,
        "type": "Loan"
    },
    {
        "title": "High-Interest Digital FD",
        "description": "Flexible fixed deposit with high interest and easy access.",
        "min_income": 50000,
        "max_risk": 90,
        "min_sentiment": 0.5,
        "type": "Savings"
    },
    {
        "title": "Eco-Friendly Cashback Card",
        "description": "Earn cashback by spending on green brands.",
        "min_income": 45000,
        "max_risk": 70,
        "min_sentiment": 0.6,
        "type": "Credit Card"
    },
    {
        "title": "Home Builder Mortgage",
        "description": "Affordable housing loan for first-time buyers.",
        "min_income": 80000,
        "max_risk": 55,
        "min_sentiment": 0.5,
        "type": "Loan"
    },
    {
        "title": "Retirement Planning Tool",
        "description": "Long-term pension & retirement saving plan.",
        "min_income": 65000,
        "max_risk": 50,
        "min_sentiment": 0.6,
        "type": "Investment"
    },
    {
        "title": "Student Essentials Card",
        "description": "Low-limit credit card for students with bonus points.",
        "min_income": 10000,
        "max_risk": 90,
        "min_sentiment": 0.4,
        "type": "Credit Card"
    },
]

def personalize_recommendation(user_id):
    sentiment = analyze_sentiment(user_id)
    risk = calculate_risk_score(user_id)

    if "error" in sentiment or "error" in risk:
        print("❌ [PERSONALIZATION] Failed to fetch risk/sentiment.")
        return {"error": "Unable to generate offers."}

    sentiment_score = sum(1 for s in sentiment["sentiment_analysis"]
                          if s["sentiment"].lower() == "positive") / len(sentiment["sentiment_analysis"]) if sentiment["sentiment_analysis"] else 0
    risk_score = risk["risk_score"]

    print(f"📊 [PERSONALIZATION] Risk Score: {risk_score}, Sentiment Score: {sentiment_score:.2f}")

    eligible_offers = []
    for offer in FINANCIAL_PRODUCTS:
        eligible = (
            risk_score <= offer["max_risk"] and
            sentiment_score >= offer["min_sentiment"]
        )
        offer_data = offer.copy()
        offer_data["recommended"] = bool(eligible)

        eligible_offers.append(offer_data)

    return {
        "user_id": user_id,
        "risk_score": round(risk_score, 2),
        "sentiment_score": round(sentiment_score, 2),
        "offers": eligible_offers
    }
