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