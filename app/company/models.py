from pydantic import BaseModel, EmailStr
from typing import List, Optional, ForwardRef
from app.role.models import Role
from bson.objectid import ObjectId
from enum import Enum

RoleRef = ForwardRef("Role")
SuperUserRef = ForwardRef("SuperUser")
BranchRef = ForwardRef("Branch")

class MobileObject(BaseModel):
    country_code: str
    number: str

class OTP(BaseModel):
    otp: str
    expires: str

class SuperUserRegister(BaseModel):
    firstname: str
    lastname: str
    email: str
    mobile: MobileObject
    dob: str
    password: str

class SuperUser(BaseModel):
    firstname: str
    lastname: str
    email: str
    mobile: MobileObject
    dob: str
    password: str
    otp: OTP = None
    verified: bool = False
    disabled: bool = False

class SuperUserOut(BaseModel):
    firstname: str
    lastname: str
    email: str
    dob: str
    mobile: MobileObject
    password: str

class Company(BaseModel):
    name: str = ""
    address: str = ""
    phone: str = ""
    description: str = ""
    email: EmailStr = ""
    branches: List[str] = []
    superusers: List[str] = []
    website: str = ""
    logo: str = ""
    attributes: dict = {}

class CompanyIn(BaseModel):
    name: str
    address: str
    phone: str
    description: str
    email: EmailStr
    website: str = ""
    logo: str = ""

class Branch(BaseModel):
    name: str
    address: str
    phone: str
    email: str
    website: str
    logo: str
    attributes: dict = {}
    company: str
