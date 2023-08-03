from bson import ObjectId
from app.db.db import db
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from app.schema.schemas import permission_serial
from app.models.role import Permission

router = APIRouter({
    "prefix": "/permission",
    "tags": ["Permission"]
})

permission = db["permission"] # collection

@router.post("/", response_description="Add new permission", response_model=Permission)
async def create_permission(permission: Permission = Depends(permission_serial)):
    try:
        permission_id = await db["permission"].insert_one(permission.dict())
        new_permission = await db["permission"].find_one({"_id": permission_id.inserted_id})
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=new_permission)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@router.get("/{permission_id}", response_description="Get a single permission", response_model=Permission)
async def read_permission(permission_id: str):
    try:
        permission = await db["permission"].find_one({"_id": ObjectId(permission_id)})
        if permission:
            return permission
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@router.put("/{permission_id}", response_description="Update a permission", response_model=Permission)
async def update_permission(permission_id: str, permission: Permission = Depends(permission_serial)):
    try:
        permission = await db["permission"].find_one({"_id": ObjectId(permission_id)})
        if permission:
            updated_permission = await db["permission"].update_one({"_id": ObjectId(permission_id)}, {"$set": permission.dict()})
            if updated_permission:
                return await db["permission"].find_one({"_id": ObjectId(permission_id)})
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to update permission")
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@router.delete("/{permission_id}", response_description="Delete a permission")
async def delete_permission(permission_id: str):
    try:
        permission = await db["permission"].find_one({"_id": ObjectId(permission_id)})
        if permission:
            await db["permission"].delete_one({"_id": ObjectId(permission_id)})
            return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={})
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))