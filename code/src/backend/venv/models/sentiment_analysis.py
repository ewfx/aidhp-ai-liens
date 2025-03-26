import os
import requests
from dotenv import load_dotenv
from db import sentiments_collection

# ✅ Resolve correct path: one level up from this file
current_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(current_dir, '..', 'key.env')
load_dotenv(env_path)

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

if not HUGGINGFACE_API_KEY:
    print("❌ [ENV] Hugging Face API Key is missing. Check the key.env path or variable name.")
else:
    print("✅ [ENV] Hugging Face API Key loaded successfully.")

MODEL_NAME = "cardiffnlp/twitter-roberta-base-sentiment"

def analyze_sentiment(user_id):
    """Fetch user social media posts and analyze sentiment using Hugging Face API."""
    print(f"🧠 [SENTIMENT] Analyzing sentiment for user: {user_id}")

    posts = list(sentiments_collection.find(
        {"Customer ID": user_id}, {"_id": 0, "Content": 1}
    ))

    if not posts:
        print("⚠️ [SENTIMENT] No social media posts found.")
        return {"error": "No social media data found for this user."}

    results = []
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    label_map = {
        "LABEL_0": "Negative",
        "LABEL_1": "Neutral",
        "LABEL_2": "Positive"
    }

    for i, post in enumerate(posts):
        if "Content" not in post:
            #print(f"⚠️ [SENTIMENT] Skipping post {i}: no 'Content' field.")
            continue

        payload = {"inputs": post["Content"]}
        #print(f"📝 [SENTIMENT] Sending to model: {post['Content']}")

        response = requests.post(
            f"https://api-inference.huggingface.co/models/{MODEL_NAME}",
            headers=headers, json=payload
        )

        if response.status_code == 200:
            output = response.json()
            #print(f"📥 [SENTIMENT] Model raw response: {output}")
            try:
                raw_label = output[0][0]["label"]
                sentiment = label_map.get(raw_label, raw_label)
            except Exception as e:
                print(f"❌ [SENTIMENT] Failed to extract sentiment. Error: {e}")
                sentiment = "Unknown"
        else:
            sentiment = "Error analyzing sentiment"
            print(f"❌ [SENTIMENT] API failed. Status: {response.status_code}, Message: {response.text}")

        results.append({
            "post": post["Content"],
            "sentiment": sentiment
        })

    # 🔍 Calculate overall sentiment breakdown
    positive = sum(1 for s in results if s["sentiment"].lower() == "positive")
    neutral = sum(1 for s in results if s["sentiment"].lower() == "neutral")
    negative = sum(1 for s in results if s["sentiment"].lower() == "negative")
    total = len(results)

    positive_ratio = positive / total if total else 0

    if positive_ratio >= 0.7:
        overall = "Mostly Positive"
    elif negative > positive:
        overall = "Mostly Negative"
    else:
        overall = "Mixed"

    print(f"📊 [SENTIMENT] Summary — Positive: {positive}, Neutral: {neutral}, Negative: {negative}")
    print(f"✅ [SENTIMENT] Overall Sentiment: {overall}, Positive Ratio: {round(positive_ratio, 2)}")

    return {
        "user_id": user_id,
        "overall_sentiment": overall,
        "positive_ratio": round(positive_ratio, 2),
        "sentiment_analysis": results
    }
