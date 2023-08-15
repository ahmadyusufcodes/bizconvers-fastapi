from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from fastapi.security import OAuth2PasswordRequestForm
from bson import ObjectId
from app.db.db import db
from app.models.role import Role
from app.models.company import Company
from app.schema.schemas import company_serializer, branch_serializer, staff_serializer
from app.utils.request_utils import response

router = APIRouter()

companies_col = db["company"]
branches_col = db["branch"]
staff_col = db["staff"]

@router.get("/", response_description="Get all companies")
async def read_companies():
    try:
        companies_list = companies_col.find()
        companies_list = [company_serializer(company) for company in companies_list]
        return response(status_code=200, message="Companies retrieved successfully", data=companies_list)
    except Exception as e:
        return response(status_code=500, message=str(e))

@router.post("/")
async def create_company(company: Company):
    try:
        company_id = companies_col.insert_one(company.dict()).inserted_id
        return response(status_code=200, message="Company created successfully", data=company_serializer(companies_col.find_one({"_id": ObjectId(company_id)})))
    except Exception as e:
        return response(status_code=500, message=str(e))

@router.get("/{company_id}")
async def get_company(company_id: str):
    try:
        find_company = companies_col.find_one({"_id": ObjectId(company_id)})
        if find_company:
            return response(status_code=200, message="Company retrieved successfully", data=company_serializer(find_company))
        else:
            return response(status_code=404, message="Company not found")
    except Exception as e:
        return response(status_code=500, message=str(e))
    
@router.put("/{company_id}")
async def update_company(company_id: str, company: Company):
    try:
        find_company = companies_col.find_one({"_id": ObjectId(company_id)})
        if not find_company:
            return response(status_code=404, message="Company not found")
        companies_col.update_one({"_id": ObjectId(company_id)}, {"$set": company.dict()})
        return response(status_code=200, message="Company updated successfully", data=company_serializer(companies_col.find_one({"_id": ObjectId(company_id)})))
    except Exception as e:
        return response(status_code=500, message=str(e))
    
@router.delete("/{company_id}")
async def delete_company(company_id: str):
    try:
        companies_col.delete_one({"_id": ObjectId(company_id)})
        return response(status_code=200, message="Company deleted successfully")
    except Exception as e:
        return response(status_code=500, message=str(e))

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
    

@router.get("/{company_id}/staff")
async def get_company_staff(company_id: str, request: Request):
    branchId = request.query_params.get('branchId')
    print(branchId, "branchId")
    print(company_id, "company_id")
    try:
        {}
        if company_id == "*":
            find_all_staff = staff_col.find()
            find_all_staff = [staff_serializer(staff) for staff in find_all_staff]
            return response(status_code=200, message="Staff retrieved successfully", data=find_all_staff)
        find_company = companies_col.find_one({"_id": ObjectId(company_id)})
        if not find_company:
            return response(status_code=404, message="Company not found")
        if branchId:
            find_branch = branches_col.find_one({"_id": ObjectId(branchId)})
            if not find_branch:
                return response(status_code=404, message="Branch not found")
            staff = staff_col.find({"company": company_id, "branch": {"$in": [branchId]}})
        else:
            staff = staff_col.find({"company": company_id})
        staff = [staff_serializer(staff) for staff in staff]
        return response(status_code=200, message="Staff retrieved successfully", data=staff)
    except Exception as e:
        return response(status_code=500, message=str(e))
