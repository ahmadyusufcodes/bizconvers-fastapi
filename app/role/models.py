from pydantic import BaseModel
from typing import List

class Permission(BaseModel):
    name: str
    read: bool
    write: bool
    delete: bool
    description: str

class Role(BaseModel):
    name: str
    description: str
    permissions: List[Permission]

class RoleOut(BaseModel):
    name: str
    description: str

class RoleRef(BaseModel):
    id: str
    name: str
    description: str