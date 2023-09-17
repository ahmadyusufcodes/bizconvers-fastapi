from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from bson import ObjectId
from app.db.db import db
from app.role.models import Role, RoleOut
from app.company.models import Company
from app.schema.schemas import role_serial
from app.utils.request_utils import response


router = APIRouter()

roles_col = db["roles"]

PERMISSION_DEFAULTS = [
    {
        "name": "users",
        "read": False,
        "write": False,
        "delete": False,
        "description": "Can view and edit users"
    },
    {
        "name": "inventory",
        "read": False,
        "write": False,
        "delete": False,
        "description": "Can view and edit inventory"
    },
    {
        "name": "branches",
        "read": False,
        "write": False,
        "delete": False,
        "description": "Can view and edit branches"
    },
    {
        "name": "companies",
        "read": False,
        "write": False,
        "delete": False,
        "description": "Can view and edit companies"
    },
    {
        "name": "roles",
        "read": False,
        "write": False,
        "delete": False,
        "description": "Can view and edit roles"
    },
    {
        "name": "staff",
        "read": False,
        "write": False,
        "delete": False,
        "description": "Can view and edit staff"
    },
    {
        "name": "superuser",
        "read": False,
        "write": False,
        "delete": False,
        "description": "Can view and edit superuser"
    }
]
@router.get("/", response_description="Get all roles")
async def read_roles():
    try:
        roles_list = list(roles_col.find({}))
        roles_list = [role_serial(role) for role in roles_list]
        return response(status_code=200, message="Roles retrieved successfully", data=roles_list)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/")
async def create_role(role: RoleOut):
    role = role.dict()
    check_name_exists = roles_col.find_one({"name": role["name"]})
    if check_name_exists:
        return response(status_code=400, message="Role name already exists", data=None)
    try:
        name: str = role["name"]
        description: str = role["description"]
        permissions: list = role["permissions"]
        role["permissions"] = permissions or PERMISSION_DEFAULTS
        saved_role = roles_col.insert_one(role)
        return response(status_code=200, message="Role created successfully", data=role_serial(roles_col.find_one({"_id": ObjectId(saved_role.inserted_id)})))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{role_id}")
async def get_role(role_id: str):
    try:
        return role_serial(roles_col.find_one({"_id": ObjectId(role_id)}))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.put("/{role_id}")
async def update_role(role_id: str, role: Role):
    try:
        roles_col.update_one({"_id": ObjectId(role_id)}, {"$set": role.dict()})
        return role_serial(roles_col.find_one({"_id": ObjectId(role_id)}))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.delete("/{role_id}")
async def delete_role(role_id: str):
    try:
        roles_col.delete_one({"_id": ObjectId(role_id)})
        return {"message": "Role deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))