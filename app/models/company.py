from pydantic import BaseModel
from typing import List, Optional, ForwardRef
from app.models.role import Role
from bson.objectid import ObjectId

RoleRef = ForwardRef("Role")
SuperUserRef = ForwardRef("SuperUser")
BranchRef = ForwardRef("Branch")

class User(BaseModel):
    username: str
    password: str
    roles: List[RoleRef] = []
    branch: Optional[BranchRef] = None

class SuperUser(BaseModel):
    username: str
    password: str
    otp: str
    roles: List[RoleRef] = []

class Company(BaseModel):
    name: str = ""
    address: str = ""
    phone: str = ""
    email: str = ""
    branches: List[str] = []
    superusers: List[str] = []
    website: str = ""
    logo: str = ""
    gstin: str = ""
    cin: str = ""
    pan: str = ""
    tan: str = ""

class Branch(BaseModel):
    name: str
    address: str
    phone: str
    email: str
    website: str
    logo: str
    gstin: str
    cin: str
    pan: str
    tan: str
    company: str

class Staff(BaseModel):
    name: str
    address: str
    phone: str
    email: str
    branch: str
    avartar: str
    roles: List[RoleRef] = []
    password: str
    username: str
    otp: str