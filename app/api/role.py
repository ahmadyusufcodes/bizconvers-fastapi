from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from bson import ObjectId
from app.db.db import db
from app.models.role import Role
from app.models.company import Company
from app.schema.schemas import role_serial


router = APIRouter()

roles = db["roles"]

@router.post("/")
async def create_role(role: Role):
    try:
        role_id = roles.insert_one(role.dict()).inserted_id
        return role_serial(roles.find_one({"_id": role_id}))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{role_id}")
async def get_role(role_id: str):
    try:
        return role_serial(roles.find_one({"_id": ObjectId(role_id)}))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.put("/{role_id}")
async def update_role(role_id: str, role: Role):
    try:
        roles.update_one({"_id": ObjectId(role_id)}, {"$set": role.dict()})
        return role_serial(roles.find_one({"_id": ObjectId(role_id)}))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.delete("/{role_id}")
async def delete_role(role_id: str):
    try:
        roles.delete_one({"_id": ObjectId(role_id)})
        return {"message": "Role deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))