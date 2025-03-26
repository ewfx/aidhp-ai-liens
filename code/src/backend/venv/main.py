from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from db import users_collection, transactions_collection, sentiments_collection
from utils import clean_user_data
from models.recommendation import generate_recommendation
from models.sentiment_analysis import analyze_sentiment
from models.risk_assessment import calculate_risk_score
from models.personalization import personalize_recommendation
from auth import router as auth_router, get_current_user

app = FastAPI()

# ✅ Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Include authentication routes
app.include_router(auth_router)

@app.get("/")
def health_check():
    return {"message": "Backend is running ✅"}

# ✅ GET all users (Protected)
@app.get("/api/users")
async def get_users(current_user: dict = Depends(get_current_user)):
    users = list(users_collection.find({}, {"_id": 0}))
    return {"users": users}

# ✅ GET transactions for a user (Protected)
@app.get("/api/transactions/{user_id}")
async def get_transactions(user_id: str, current_user: dict = Depends(get_current_user)):
    if current_user["Customer ID"].lower() != user_id.lower():
        raise HTTPException(status_code=403, detail="Unauthorized access")

    transactions = list(transactions_collection.find({"Customer ID": user_id}, {"_id": 0}))
    if not transactions:
        raise HTTPException(status_code=404, detail="No transactions found")
    return {"transactions": transactions}

# ✅ POST new transaction (Protected)
@app.post("/api/transactions")
async def add_transaction(transaction: dict, current_user: dict = Depends(get_current_user)):
    if "Customer ID" not in transaction or "amount" not in transaction:
        raise HTTPException(status_code=400, detail="Missing required fields")

    if current_user["Customer ID"].lower() != transaction["Customer ID"].lower():
        raise HTTPException(status_code=403, detail="Unauthorized transaction")

    transactions_collection.insert_one(transaction)
    return {"message": "Transaction added successfully"}

# ✅ POST feedback (Protected)
@app.post("/api/feedback")
async def add_feedback(feedback: dict, current_user: dict = Depends(get_current_user)):
    if "Customer ID" not in feedback or "message" not in feedback:
        raise HTTPException(status_code=400, detail="Missing required fields")

    if current_user["Customer ID"].lower() != feedback["Customer ID"].lower():
        raise HTTPException(status_code=403, detail="Unauthorized feedback")

    sentiments_collection.insert_one(feedback)
    return {"message": "Feedback recorded"}

# ✅ Sentiment Analysis API (Protected)
@app.get("/api/sentiment/{user_id}")
async def sentiment(user_id: str, current_user: dict = Depends(get_current_user)):
    print("📊 [SENTIMENT] user_id from URL:", repr(user_id))
    print("🔐 [SENTIMENT] Customer ID from token:", repr(current_user.get("Customer ID")))
    
    if current_user["Customer ID"].lower() != user_id.lower():
        print("❌ [SENTIMENT] Unauthorized access attempt")
        raise HTTPException(status_code=403, detail="Unauthorized access")
    
    return analyze_sentiment(user_id)

# ✅ Risk Assessment API (Protected)
@app.get("/api/risk/{user_id}")
async def risk(user_id: str, current_user: dict = Depends(get_current_user)):
    if current_user["Customer ID"].lower() != user_id.lower():
        raise HTTPException(status_code=403, detail="Unauthorized access")
    return calculate_risk_score(user_id)

# ✅ Personalized Offers API (Protected)
@app.get("/api/personalize/{user_id}")
async def personalize(user_id: str, current_user: dict = Depends(get_current_user)):
    if current_user["Customer ID"].lower() != user_id.lower():
        raise HTTPException(status_code=403, detail="Unauthorized access")
    return personalize_recommendation(user_id)

# ✅ Recommendation API (Protected)
@app.get("/api/recommend/{user_id}")
async def recommend(user_id: str, current_user: dict = Depends(get_current_user)):
    if current_user["Customer ID"].lower() != user_id.lower():
        raise HTTPException(status_code=403, detail="Unauthorized access")
    return generate_recommendation(user_id)

# ✅ Server entry point
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
