import os
import requests
from dotenv import load_dotenv
from db import sentiments_collection, users_collection, transactions_collection

# ✅ Resolve correct path: one level up from this file
current_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(current_dir, '..', 'key.env')
load_dotenv(env_path)
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

if not HUGGINGFACE_API_KEY:
    print("❌ [ENV] Hugging Face API Key is missing. Check the key.env path or variable name.")
else:
    print("✅ [ENV] Hugging Face API Key loaded successfully.")

MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.1"

def get_user_data(user_id):
    """Fetch user profile and transaction history from MongoDB."""
    user = users_collection.find_one({"Customer ID": user_id}, {"_id": 0})
    transactions = list(transactions_collection.find({"Customer ID": user_id}, {"_id": 0}))

    if not user:
        return None

    return {"profile": user, "transactions": transactions}

def generate_recommendation(user_id):
    """Generate personalized financial product recommendations."""
    print(f"📥 [RECOMMEND] Fetching data for user: {user_id}")
    user_data = get_user_data(user_id)
    if not user_data:
        print("❌ [RECOMMEND] User not found.")
        return {"error": "User not found."}

    profile = user_data["profile"]
    transactions = user_data["transactions"]

    print(f"✅ [RECOMMEND] Retrieved profile and {len(transactions)} transactions.")

    # Gather contextual details
    age = profile.get("Age", "N/A")
    income = profile.get("Income", "N/A")
    occupation = profile.get("Occupation", "N/A")
    interests = profile.get("Interests", "Not provided")
    education = profile.get("Education", "Not provided")
    preferences = profile.get("Preferences", "Not provided")

    # Prepare enriched prompt
    prompt = f"""
    Based on the following user's profile and their past behavior,I suggest a personalized financial product (loan, investment, credit card, etc.) with the following features that would best suit the user's needs and preferences:

    User Profile:
    - Age: {age}
    - Income: {income}
    - Occupation: {occupation}
    - Education: {education}
    - Interests: {interests}
    - Preferences: {preferences}
    - Number of Past Transactions: {len(transactions)}
    """

    print(f"🧠 [RECOMMEND] Prompt for model:\n{prompt}")

    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    payload = {"inputs": prompt, "parameters": {"max_length": 300}}

    response = requests.post(
        f"https://api-inference.huggingface.co/models/{MODEL_NAME}",
        headers=headers,
        json=payload
    )

    if response.status_code == 200:
        result = response.json()[0]['generated_text']
        print("✅ [RECOMMEND] Recommendation generated successfully.")
        return {"recommendation": result}
    else:
        print(f"❌ [RECOMMEND] API call failed. Status {response.status_code}: {response.text}")
        return {"error": response.json()}
