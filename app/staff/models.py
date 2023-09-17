from typing import List
from pydantic import BaseModel
from app.role.models import RoleRef

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