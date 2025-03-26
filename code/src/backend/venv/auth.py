from fastapi import APIRouter, HTTPException, Header
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from db import people_collection
from dotenv import load_dotenv
import os
from pathlib import Path
import bcrypt
from passlib.context import CryptContext
import re

router = APIRouter()

MAX_CUSTOMERS = 1000

def get_password_hash(password):
    return pwd_context.hash(password)

# Load .env using an absolute path
dotenv_path = Path(__file__).parent / "key.env"
load_dotenv(dotenv_path)

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))


if not SECRET_KEY:
    raise Exception(" SECRET_KEY not found. Check your .env file or load_dotenv path.")

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(authorization: str = Header(...)):
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid token scheme")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except (JWTError, ValueError):
        raise HTTPException(status_code=401, detail="Invalid or expired token")

@router.post("/login")
async def login(data: dict):
    email = data.get("email", "").strip().lower()
    password = data.get("password", "").strip()

    user = people_collection.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user["email"], "Customer ID": user["Customer ID"]})
    return {"access_token": token, "Customer ID": user["Customer ID"]}



# Utility to hash password
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

@router.post("/register")
def register_user(data: dict):
    customer_id = data.get("customer_id")
    email = data.get("email")
    password = data.get("password")

    if not all([customer_id, email, password]):
        raise HTTPException(status_code=400, detail="All fields are required")

    # Validate Customer ID format
    if not re.fullmatch(r"CUST\d{4}", customer_id):
        raise HTTPException(status_code=400, detail="Customer ID must be in CUST0000 format")

    # Ensure within allowed range
    customer_num = int(customer_id[4:])
    if customer_num >= MAX_CUSTOMERS:
        raise HTTPException(status_code=400, detail="Customer ID limit exceeded")

    # Check if ID already taken
    if people_collection.find_one({"customer_id": customer_id}):
        raise HTTPException(status_code=400, detail="Customer ID already exists")

    # Hash and store
    password_hash = hash_password(password)
    people_collection.insert_one({
        "Customer ID": customer_id,
        "email": email,
        "hashed_password":get_password_hash(password)
    })

    return {"message": "User registered successfully"}
