import numpy as np
from db import transactions_collection, users_collection

def calculate_risk_score(user_id):
    """Determine financial risk based on spending patterns and customer income."""

    print(f"📊 [RISK] Calculating risk score for user: {user_id}")

    # Fetch transactions for the user
    transactions = list(transactions_collection.find(
        {"Customer ID": user_id},
        {"_id": 0}
    ))

    if not transactions:
        print("⚠️ [RISK] No transactions found.")
        return {"error": "No transactions found for this user."}

    # Fetch income from customer profile
    user_profile = users_collection.find_one({"Customer ID": user_id})
    if not user_profile or "Income" not in user_profile:
        print("⚠️ [RISK] User profile or income not found.")
        return {"error": "User profile or income not found."}

    income = user_profile["Income"]
    print(f"💰 [RISK] Income from profile: {income}")

    # Calculate total spending for in-store transactions
    total_spent = sum(
        t.get("Amount", 0) for t in transactions
    )
    print(f"🛍️ [RISK] Total in-store spending: {total_spent}")

    # Risk logic: higher spend relative to income = higher risk
    risk_score = 100 - ((income - total_spent) / (income + 1)) * 100
    risk_score = np.clip(risk_score, 0, 100)

    print(f"✅ [RISK] Final Risk Score: {risk_score}")

    return {"risk_score": round(risk_score, 2)}

