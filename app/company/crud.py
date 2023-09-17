from app.company.models import Company, Branch
from app.db.db import db

company_col = db["companies"]
branch_col = db["branches"]

async def create_company(company: Company):
    company = company.dict()
    company_col.insert_one(company)
    return company

async def get_company(company_id: str):
    company = company_col.find_one({"_id": company_id})
    return company

async def get_companies():
    companies = company_col.find()
    return companies

async def update_company(company_id: str, company: Company):
    company = company.dict()
    company_col.update_one({"_id": company_id}, {"$set": company})
    return company

async def delete_company(company_id: str):
    company_col.delete_one({"_id": company_id})
    return company_id

async def create_branch(company_id: str, branch: Branch):
    branch = branch.dict()
    branch_col.insert_one(branch)
    return branch

async def get_branch(company_id: str, branch_id: str):
    branch = branch_col.find_one({"_id": branch_id})
    return branch

async def get_branches(company_id: str):
    branches = branch_col.find()
    return branches

async def update_branch(company_id: str, branch_id: str, branch: Branch):
    branch = branch.dict()
    branch_col.update_one({"_id": branch_id}, {"$set": branch})
    return branch

async def delete_branch(company_id: str, branch_id: str):
    branch_col.delete_one({"_id": branch_id})
    return branch_id