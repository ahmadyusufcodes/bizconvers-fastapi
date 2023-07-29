import os
from fastapi import FastAPI
from app.api.auth import router as auth_router
app = FastAPI()
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
load_dotenv()

# Basic route
@app.get("/")
def read_root():
    return {"Hello": "World"}
# main.py
from fastapi import FastAPI

app = FastAPI()

DB_URL = os.environ.get("MONGO_URL")

client = MongoClient(DB_URL)
db = client["rumbu"]
try:
    client.server_info()
    print("Connected to MongoDB 🚀")
except:
    print("Could not connect to MongoDB")


# Basic route
@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(auth_router, prefix="/api/auth", tags=["auth"])