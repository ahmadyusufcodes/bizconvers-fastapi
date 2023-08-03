from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from datetime import timedelta
from app.utils.perms_utils import verify_is_admin
from app.db.db import db
from app.utils.jwt_utils import create_jwt_token, verify_jwt_token
from os import environ
import json
from app.models.company import Company, Branch, SuperUser, Staff
from app.schemas import UserCredentials, Role, Permission, SuperUser
from app.utils.password_utils import hash_password, verify_password
from app.models.user import User
from bson import ObjectId
from app.api.auth import authenticate_user
from app.schema.schemas import permission_serial, role_serial
from app.utils.request_utils import success_response, error_response

router = APIRouter()
superuser = db["superuser"]

SECRET_KEY = environ.get("SECRET_KEY")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

@router.post("/register/superuser")
async def register_superuser(super_user: SuperUser):
    # use try catch to check if superuser exists
    try:
        hashed_password = hash_password(super_user.password)
        superuser.insert_one({"username": super_user.username, "email": super_user.email, "password": hashed_password})
        return success_response({"message": "Superuser created successfully", "username": dict(super_user)})
    except Exception as e:
        return error_response(str(e))
    
@router.post("/register/user")
async def register_user(staff: Staff):
    try:
        hashed_password = hash_password(staff.password)
        staff.password = hashed_password
        superuser.insert_one(staff.dict())
        return success_response({"message": "Superuser created successfully", "username": dict(staff)})
    except Exception as e:
        return error_response(str(e))
    
@router.post("/login")
async def login(userCreds: UserCredentials):
    user = authenticate_user(userCreds.username, userCreds.password)
    if user:
        token_data = {"sub": user["username"], "roles": user["roles"]}
        access_token_expires = timedelta(minutes=30)
        access_token = create_jwt_token(token_data, access_token_expires)
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
@router.get("/users")
# paginated
async def get_users(request: Request):
    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 10, type=int)
    try:
        users = db.users.find().skip((page - 1) * limit).limit(limit)
        return success_response({"users": [user for user in users], "total": users.count(), "page": page, "limit": limit})
    except Exception as e:
        return error_response(str(e))

@router.get("/users/{user_id}")
async def get_user(user_id: str):
    try:
        user = db.users.find_one({"_id": ObjectId(user_id)})
        return success_response({"user": user})
    except Exception as e:
        return error_response(str(e))

@router.put("/users/{user_id}")
async def update_user(user_id: str, user: User):
    try:
        db.users.update_one({"_id": ObjectId(user_id)}, {"$set": user.dict()})
        return success_response({"message": "User updated successfully"})
    except Exception as e:
        return error_response(str(e))

@router.delete("/users/{user_id}")
async def delete_user(user_id: str):
    try:
        db.users.delete_one({"_id": ObjectId(user_id)})
        return success_response({"message": "User deleted successfully"})
    except Exception as e:
        return error_response(str(e))