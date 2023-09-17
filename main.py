import os
import typing as t
from fastapi import Depends, FastAPI, HTTPException, Response
# from app.api.auth import router as auth_router
from app.api.company import router as company_router
from app.api.branch import router as branch_router
from app.api.staff import router as staff_router
from app.api.role import router as role_router
from app.api.product import router as product_router
from app.api.authentication import router as authentication_router
from app.utils.request_utils import response
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security.http import HTTPAuthorizationCredentials, HTTPBearer

# We will handle a missing token ourselves
get_bearer_token = HTTPBearer(auto_error=False)

known_tokens = set(["api_token_abc123"])

async def get_token(
    auth: t.Optional[HTTPAuthorizationCredentials] = Depends(get_bearer_token),
) -> str:
    # Simulate a database query to find a known token
    if auth is None or (token := auth.credentials) not in known_tokens:
        return response(status_code=401, message="Invalid token", data=None)
    return token

DB_URL = os.environ.get("MONGO_URL")

app = FastAPI()
load_dotenv()

# Define your CORS configuration
origins = ["*"]

# Add the CORS middleware to your app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


client = MongoClient(DB_URL)
db = client["rumbu"]
try:
    client.server_info()
    print("Connected to MongoDB 🚀")
except:
    print("Couldn't connect to MongoDB 😢")


# Basic route
@app.get("/", tags=["Connection Test"])
def read_root():
    return {"Hello": "World"}

@app.get("/protected", response_model=str)
async def protected(token: str = Depends(get_token)):
    print(token)
    if token is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return f"Hello, user! Your token is {token}."

app.include_router(authentication_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(staff_router, prefix="/api/staff", tags=["Staff"], dependencies=[Depends(get_token)])
app.include_router(company_router, prefix="/api/company", tags=["Company"], dependencies=[Depends(get_token)])
app.include_router(branch_router, prefix="/api/branch", tags=["Branch"], dependencies=[Depends(get_token)])
app.include_router(product_router, prefix="/api/product", tags=["Product"], dependencies=[Depends(get_token)])
# app.include_router(auth_router, prefix="/api/auth", tags=["Auth"], dependencies=[Depends(get_token)])
app.include_router(role_router, prefix="/api/role", tags=["Role"], dependencies=[Depends(get_token)])