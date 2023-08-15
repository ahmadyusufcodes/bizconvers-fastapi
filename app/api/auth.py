from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from datetime import timedelta
from app.utils.perms_utils import verify_is_admin
from app.db.db import db
from app.utils.jwt_utils import create_jwt_token, verify_jwt_token
from os import environ
import json
from app.schemas import UserCredentials, Role, Permission
from app.utils.password_utils import hash_password, verify_password
from app.models.company import SuperUser, Staff
from bson import ObjectId
from app.schema.schemas import permission_serial, role_serial
from app.utils.request_utils import response

router = APIRouter()
superuser = db["superuser"]
staff = db["staff"]

SECRET_KEY = environ.get("SECRET_KEY")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def authenticate_user(username: str, password: str):
    check_super_user = superuser.find_one({"username": username})
    check_staff = staff.find_one({"username": username})
    if check_super_user:
        if  (password, check_super_user["password"]):
            return check_super_user
        else:
            return "Invalid credentials"
    elif check_staff:
        if verify_password(password, check_staff["password"]):
            return check_staff
        else:
            return "Invalid credentials"
    else:
        return "Invalid credentials"

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

@router.get("/protected")
async def protected_route(token: str = Depends(oauth2_scheme)):
    payload = verify_jwt_token(token)
    if payload:
        return {"message": "This is a protected route!", "user": payload["sub"], "roles": payload["roles"]}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

@router.get("/adminroute")
def admin_route(data: dict = Depends(verify_is_admin)):
    return data

@router.post("/register")
async def register(userCreds: UserCredentials):
    user = db.users.find_one({"username": userCreds.username})
    print(user)
    if user:
        return {"error": "User already exists", }
    else:
        hashed_password = hash_password(userCreds.password)
        db.users.insert_one({"username": userCreds.username, "password": hashed_password})

@router.get("/roles")
async def get_roles():
    try:
        roles = db.roles.find()
        return  response(status.HTTP_200_OK, "Roles fetched successfully", [role_serial(role) for role in roles])
    except Exception as e:
        return response(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))  

@router.post("/roles")
def create_role(request: Role):
    try:
        role = db.roles.insert_one(request.dict(by_alias=True))
        return response(status.HTTP_201_CREATED, "Role created successfully", role_serial(db.roles.find_one({"_id": role.inserted_id})))
    except Exception as e:
        return response(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))

