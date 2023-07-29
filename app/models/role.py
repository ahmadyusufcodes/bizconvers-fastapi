from pydantic import BaseModel

class Role(BaseModel):
    name: str
    description: str
    permissions: list

class Permission(BaseModel):
    name: str
    read: bool
    write: bool
    description: str

