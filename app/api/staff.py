from bson import ObjectId
from app.db.db import db
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from app.schema.schemas import staff_serializer, staff_update_serializer
from app.models.company import Staff, Branch
from app.utils.jwt_utils import create_jwt_token, verify_jwt_token
from app.utils.password_utils import verify_password, hash_password
from pymongo.errors import DuplicateKeyError


router = APIRouter()

staff = db["staff"]

@router.post("/", response_description="Add new staff", response_model=Staff)
def create_staff(staff: Staff):
    try:
        staff = staff.dict()
        staff["password"] = hash_password(staff["password"])
        staff_id = db["staff"].insert_one(staff)
        new_staff = db["staff"].find_one({"_id": staff_id.inserted_id})
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=staff_serializer(new_staff))
    except DuplicateKeyError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Staff with this email already exists")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/{staff_id}", response_description="Get a single staff", response_model=Staff)
async def read_staff(staff_id: str):
    try:
        staff = await db["staff"].find_one({"_id": ObjectId(staff_id)})
        if staff:
            return staff
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Staff not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/{staff_id}", response_description="Update a staff", response_model=Staff)
async def update_staff(staff_id: str, staff: Staff):
    try:
        find_staff = await db["staff"].find_one({"_id": ObjectId(staff_id)})
        if find_staff:
            updated_staff = await db["staff"].update_one({"_id": ObjectId(staff_id)}, {"$set": staff.dict()})
            if updated_staff:
                return await db["staff"].find_one({"_id": ObjectId(staff_id)})
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to update staff")
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Staff not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/{staff_id}", response_description="Delete a staff")
async def delete_staff(staff_id: str):
    try:
        staff = await db["staff"].find_one({"_id": ObjectId(staff_id)})
        if staff:
            await db["staff"].delete_one({"_id": ObjectId(staff_id)})
            return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={})
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Staff not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/branch/{branch_id}", response_description="Get all staff in a branch")
async def read_staff_by_branch(branch_id: str):
    try:
        branch = await db["branch"].find_one({"_id": ObjectId(branch_id)})
        if branch:
            staff = await db["staff"].find({"branch": branch_id}).to_list(length=100)
            return staff
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Branch not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@router.get("/branch/{branch_id}/role/{role_id}/{page}", response_description="Get all staff in a branch with a role")
async def read_staff_by_branch_and_role(branch_id: str, role_id: str, page: int):
    try:
        branch = await db["branch"].find_one({"_id": ObjectId(branch_id)})
        if branch:
            total = await db["staff"].count_documents({"branch": branch_id, "roles": {"$elemMatch": {"_id": ObjectId(role_id)}}})
            staff = await db["staff"].find({"branch": branch_id, "roles": {"$elemMatch": {"_id": ObjectId(role_id)}}}).skip((page - 1) * 10).limit(10).to_list(length=100)
            return {"total": total, "staff": staff, "next": page + 1}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Branch not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/role/{role_id}/{page}", response_description="Get all staff with a role")
async def read_staff_by_role(role_id: str, page: int, request: Request):
    try:
        total = await db["staff"].count_documents({"roles": {"$elemMatch": {"_id": ObjectId(role_id)}}})
        staff = await db["staff"].find({"roles": {"$elemMatch": {"_id": ObjectId(role_id)}}}).skip((page - 1) * 10).limit(10).to_list(length=100)
        return {"total": total, "staff": staff, "next": page + 1}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

