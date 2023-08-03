from pydantic import BaseModel
from typing import List, Optional, ForwardRef
from app.models.role import Role
from bson import ObjectId

RoleRef = ForwardRef("Role")

class User(BaseModel):
    username: str
    password: str
    roles: List[RoleRef] = []
    branch: Optional[str] = None

class SuperUser(BaseModel):
    username: str
    password: str
    otp: str
    roles: List[RoleRef] = []

class Company(BaseModel):
    name: str
    address: str
    phone: str
    email: str
    branches: Optional[ObjectId] = None
    superuser: Optional[ObjectId] = None
    website: str
    logo: str
    gstin: str
    cin: str
    pan: str
    tan: str

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
    company: ObjectId

class Staff(BaseModel):
    name: str
    address: str
    phone: str
    email: str
    branch: ObjectId
    avartar: str
    roles: List[ObjectId]
    user: ObjectId
    password: str
    username: str
    otp: str