from pydantic import BaseModel
from typing import List

class Permission(BaseModel):
    name: str
    read: bool
    write: bool
    description: str

class Role(BaseModel):
    name: str
    description: str
    permissions: List[Permission]

