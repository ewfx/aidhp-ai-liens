from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["fintech_db"]

#Collections are created for the various tables under analysis
people_collection = db["users"]
users_collection = db["customer_profiles"]
transactions_collection = db["social_sentiments"]
sentiments_collection = db["transactions"]
