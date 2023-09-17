from fastapi import APIRouter, Depends, HTTPException, status, Request
from app.utils.jwt_utils import verify_jwt_token
from app.db.db import db

def verify_is_admin(request: Request):
    return verify_roles(request, ["admin"])

def verify_roles(request: Request, roles: list):
    auth_header = request.headers.get("Authorization")
    if auth_header:
        token = auth_header.split(" ")[1]
        payload = verify_jwt_token(token)
        if payload:
            if "admin" in payload["roles"]:
                return {"message": "This is an admin route!", "user": payload["sub"], "roles": payload["roles"]}
            else:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not an admin")
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

def check_permission(request: Request, action: str):
    user_permissions = db.permissions.find_one({"user_id": request.user})
    if user_permissions:
        if action in user_permissions["permissions"]:
            return True
        else:
            return False

def verify_super_admin(request: Request):
    auth_header = request.headers.get("Authorization")
    if auth_header:
        token = auth_header.split(" ")[1]
        payload = verify_jwt_token(token)
        if payload:
            if "superuser" in payload["roles"]:
                # request["user"] = payload["sub"]
                return True
            else:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not a superuser")
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    

def get_current_user(request: Request):
    auth_header = request.headers.get("Authorization")
    if auth_header:
        token = auth_header.split(" ")[1]
        payload = verify_jwt_token(token)
        if payload:
            request["user"] = payload["sub"]
            return payload["sub"]
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")