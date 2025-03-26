import pandas as pd
from db import users_collection, transactions_collection, sentiments_collection

# File paths (Modify paths as needed)
file_paths = {
    "customer_profiles": "code/src/backend/venv/data/CustomerProfile - 1.csv",
    "transactions": "code/src/backend/venv/data/Expanded_SocialMediaSentiment.csv",
    "social_sentiments": "code/src/backend/venv/data/Expanded_TransactionHistory.csv"
}

# Function to load CSV data into MongoDB
def load_csv_to_mongodb(file_path, collection):
    df = pd.read_csv(file_path)  # Read CSV file
    data = df.to_dict(orient="records")  # Convert to dictionary format
    collection.insert_many(data)  # Insert into MongoDB
    print(f"✅ Successfully inserted {len(data)} records into {collection.name}")

# Load datasets
load_csv_to_mongodb(file_paths["customer_profiles"], users_collection)
load_csv_to_mongodb(file_paths["transactions"], transactions_collection)
load_csv_to_mongodb(file_paths["social_sentiments"], sentiments_collection)

print("Data successfully loaded into MongoDB!")
