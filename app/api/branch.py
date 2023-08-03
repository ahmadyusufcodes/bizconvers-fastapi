from bson import ObjectId
from app.db.db import db
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from app.schema.schemas import branch_serializer, branch_update_serializer
from app.models.company import Branch


router = APIRouter({
    "prefix": "/branch",
    "tags": ["Branch"]
})

branch = db["branch"] # collection

@router.post("/", response_description="Add new branch", response_model=Branch)
async def create_branch(branch: Branch = Depends(branch_serializer)):
    try:
        branch_id = await db["branch"].insert_one(branch.dict())
        new_branch = await db["branch"].find_one({"_id": branch_id.inserted_id})
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=new_branch)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@router.get("/{branch_id}", response_description="Get a single branch", response_model=Branch)
async def read_branch(branch_id: str):
    try:
        branch = await db["branch"].find_one({"_id": ObjectId(branch_id)})
        if branch:
            return branch
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Branch not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@router.put("/{branch_id}", response_description="Update a branch", response_model=Branch)
async def update_branch(branch_id: str, branch: Branch = Depends(branch_update_serializer)):
    try:
        branch = await db["branch"].find_one({"_id": ObjectId(branch_id)})
        if branch:
            updated_branch = await db["branch"].update_one({"_id": ObjectId(branch_id)}, {"$set": branch.dict()})
            if updated_branch:
                return await db["branch"].find_one({"_id": ObjectId(branch_id)})
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to update branch")
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Branch not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@router.delete("/{branch_id}", response_description="Delete a branch")
async def delete_branch(branch_id: str):
    try:
        branch = await db["branch"].find_one({"_id": ObjectId(branch_id)})
        if branch:
            await db["branch"].delete_one({"_id": ObjectId(branch_id)})
            return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={})
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Branch not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))