from pydantic import BaseModel
from typing import List, Optional, ForwardRef
from app.models.role import Role
from bson.objectid import ObjectId

RoleRef = ForwardRef("Role")
SuperUserRef = ForwardRef("SuperUser")
BranchRef = ForwardRef("Branch")

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
    attributes: dict = {}

class Branch(BaseModel):
    name: str
    address: str
    phone: str
    email: str
    website: str
    logo: str
    attributes: dict = {}
    company: str

class Staff(BaseModel):
    name: str
    address: str
    phone: str
    email: str
    branch: List[str] = []
    avartar: str
    roles: List[RoleRef] = []
    password: str
    username: str
    company: str
    otp: str