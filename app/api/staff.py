from bson import ObjectId
from app.db.db import db
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from app.schema.schemas import staff_serializer, staff_update_serializer
from app.models.company import Staff, Branch
from app.utils.jwt_utils import create_jwt_token, verify_jwt_token
from app.utils.password_utils import verify_password, hash_password
from pymongo.errors import DuplicateKeyError
from app.utils.request_utils import response


router = APIRouter()

staff_col = db["staff"]
companies_col = db["company"]
branches_col = db["branch"]

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
    
@router.post("/{company_id}/staff")
async def create_company_staff(company_id: str, staff: Staff):
    try:
        find_company = companies_col.find_one({"_id": ObjectId(company_id)})
        if not find_company:
            return response(status_code=404, message="Company not found")
        staff.company = company_id
        staff_id = staff_col.insert_one(staff.dict()).inserted_id
        return response(status_code=200, message="Staff created successfully", data=staff_serializer(staff_col.find_one({"_id": ObjectId(staff_id)})))
    except Exception as e:
        return response(status_code=500, message=str(e))

@router.put("/{company_id}/staff/{staff_id}")
async def update_company_staff(company_id: str, staff_id: str, staff: Staff):
    try:
        find_company = companies_col.find_one({"_id": ObjectId(company_id)})
        if not find_company:
            return response(status_code=404, message="Company not found")
        find_staff = staff_col.find_one({"_id": ObjectId(staff_id)})
        if not find_staff:
            return response(status_code=404, message="Staff not found")
        staff_col.update_one({"_id": ObjectId(staff_id)}, {"$set": staff.dict()})
        return response(status_code=200, message="Staff updated successfully", data=staff_serializer(staff_col.find_one({"_id": ObjectId(staff_id)})))
    except Exception as e:
        return response(status_code=500, message=str(e))
    
@router.delete("/{company_id}/staff/{staff_id}")
async def delete_company_staff(company_id: str, staff_id: str):
    try:
        find_company = companies_col.find_one({"_id": ObjectId(company_id)})
        if not find_company:
            return response(status_code=404, message="Company not found")
        find_staff = staff_col.find_one({"_id": ObjectId(staff_id)})
        if not find_staff:
            return response(status_code=404, message="Staff not found")
        staff_col.delete_one({"_id": ObjectId(staff_id)})
        return response(status_code=200, message="Staff deleted successfully")
    except Exception as e:
        return response(status_code=500, message=str(e))