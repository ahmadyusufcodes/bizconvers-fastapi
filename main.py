import os
from fastapi import FastAPI
from app.api.auth import router as auth_router
from app.api.company import router as company_router
from app.api.staff import router as staff_router
from app.api.role import router as role_router
from app.api.branch import router as branch_router
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient

app = FastAPI()
load_dotenv()

# Basic route
@app.get("/health")
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

app.include_router(auth_router, prefix="/api/auth", tags=["Auth"])
app.include_router(company_router, prefix="/api/company", tags=["Company"])
app.include_router(branch_router, prefix="/api/branch", tags=["Branch"])
app.include_router(role_router, prefix="/api/role", tags=["Role"])
app.include_router(staff_router, prefix="/api/staff", tags=["Staff"])