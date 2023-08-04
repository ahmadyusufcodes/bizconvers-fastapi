from bson import ObjectId
from app.db.db import db
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from app.schema.schemas import branch_serializer, branch_update_serializer, company_serializer
from app.models.company import Branch
from app.utils.request_utils import error_response, success_response


router = APIRouter()

company = db["company"]

@router.get("/", response_description="Get all branches")
def read_branches():
    try:
        branches = db["branch"].find()
        branches = [branch_serializer(branch) for branch in branches]
        return success_response(branches)
    except Exception as e:
        return error_response(str(e))

@router.post("/", response_description="Add new branch")
async def create_branch(branch: Branch):
    branch = branch.dict()
    companyId = branch["company"]
    if not companyId:
        return error_response("Company is required")
    find_company = db["company"].find_one({"_id": ObjectId(companyId)})
    if find_company:
        try:
            branch_id = db["branch"].insert_one(branch).inserted_id
            new_branch = db["branch"].find_one({"_id": ObjectId(branch_id)})
            db["company"].update_one({"_id": ObjectId(companyId)}, {"$push": {"branches": str(branch_id)}})
            return success_response(branch_serializer(new_branch))
        except Exception as e:
            return error_response("Error occured while creating branch")
    else:
        return error_response("Company not found")
    
@router.get("/{branch_id}", response_description="Get a single branch", response_model=Branch)
async def read_branch(branch_id: str):
    try:
        branch = await db["branch"].find_one({"_id": ObjectId(branch_id)})
        if branch:
            return success_response(branch_serializer(branch))
        else:
            return error_response("Branch not found")
    except Exception as e:
        return error_response(str(e))
    
@router.put("/{branch_id}", response_description="Update a branch", response_model=Branch)
async def update_branch(branch_id: str, branch: Branch = Depends(branch_update_serializer)):
    if not branch.company:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Company is required")
    find_company = await db["company"].find_one({"_id": ObjectId(branch.company)})
    if not find_company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
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
        branch = db["branch"].find_one({"_id": ObjectId(branch_id)})
        if branch:
            deleted_branch = db["branch"].delete_one({"_id": ObjectId(branch_id)})
            if deleted_branch:
                return success_response("Branch deleted successfully")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to delete branch")
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Branch not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))