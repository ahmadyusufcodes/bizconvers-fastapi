from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from bson import ObjectId
from app.db.db import db
from app.models.role import Role
from app.models.company import Company
from app.schema.schemas import company_serializer

router = APIRouter()

companies = db["company"]

@router.get("/", response_description="Get all companies")
async def read_companies():
    try:
        companies_list = companies.find()
        companies_list = [company_serializer(company) for company in companies_list]
        return companies_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/")
async def create_company(company: Company):
    try:
        company_id = companies.insert_one(company.dict()).inserted_id
        return company_serializer(companies.find_one({"_id": company_id}))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{company_id}")
async def get_company(company_id: str):
    try:
        return company_serializer(companies.find_one({"_id": ObjectId(company_id)}))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.put("/{company_id}")
async def update_company(company_id: str, company: Company):
    try:
        companies.update_one({"_id": ObjectId(company_id)}, {"$set": company.dict()})
        return company_serializer(companies.find_one({"_id": ObjectId(company_id)}))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.delete("/{company_id}")
async def delete_company(company_id: str):
    try:
        companies.delete_one({"_id": ObjectId(company_id)})
        return {"message": "Company deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
