from bson import ObjectId
from app.db.db import db
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from app.schema.schemas import branch_serializer, branch_update_serializer, company_serializer
from app.company.models import Branch
from app.utils.request_utils import response

router = APIRouter()

branches_col = db["branch"]
companies_col = db["company"]

@router.get("/{company_id}/branch")
async def get_company_branches(company_id: str):
    try:
        find_company = companies_col.find_one({"_id": ObjectId(company_id)})
        if not find_company:
            return response(status_code=404, message="Company not found")
        branches = branches_col.find({"company": company_id})
        branches = [branch_serializer(branch) for branch in branches]
        return response(status_code=200, message="Branches retrieved successfully", data=branches)
    except Exception as e:
        return response(status_code=500, message=str(e))

@router.post("/{company_id}/branch")
async def create_company_branch(company_id: str, branch: Branch):
    try:
        find_company = companies_col.find_one({"_id": ObjectId(company_id)})
        if not find_company:
            return response(status_code=404, message="Company not found")
        branch.company = company_id
        branch_id = branches_col.insert_one(branch.dict()).inserted_id
        return response(status_code=200, message="Branch created successfully", data=branch_serializer(branches_col.find_one({"_id": ObjectId(branch_id)})))
    except Exception as e:
        return response(status_code=500, message=str(e))
    
@router.put("/{company_id}/branch/{branch_id}")
async def update_company_branch(company_id: str, branch_id: str, branch: Branch):
    try:
        find_company = companies_col.find_one({"_id": ObjectId(company_id)})
        if not find_company:
            return response(status_code=404, message="Company not found")
        find_branch = branches_col.find_one({"_id": ObjectId(branch_id)})
        if not find_branch:
            return response(status_code=404, message="Branch not found")
        branches_col.update_one({"_id": ObjectId(branch_id)}, {"$set": branch.dict()})
        return response(status_code=200, message="Branch updated successfully", data=branch_serializer(branches_col.find_one({"_id": ObjectId(branch_id)})))
    except Exception as e:
        return response(status_code=500, message=str(e))
    
@router.delete("/{company_id}/branch/{branch_id}")
async def delete_company_branch(company_id: str, branch_id: str):
    try:
        find_company = companies_col.find_one({"_id": ObjectId(company_id)})
        if not find_company:
            return response(status_code=404, message="Company not found")
        find_branch = branches_col.find_one({"_id": ObjectId(branch_id)})
        if not find_branch:
            return response(status_code=404, message="Branch not found")
        branches_col.delete_one({"_id": ObjectId(branch_id)})
        return response(status_code=200, message="Branch deleted successfully")
    except Exception as e:
        return response(status_code=500, message=str(e))
    
