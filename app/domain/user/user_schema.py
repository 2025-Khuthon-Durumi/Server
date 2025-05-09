from enum import Enum

from pydantic import BaseModel


class Role(Enum):
    FARMER = "FARMER"
    EXPERT = "EXPERT"


class UserResponse(BaseModel):
    id: int
    name: str
    phone: str
    role: Role


class UserRequest(BaseModel):
    name: str
    role: Role
    phone: str
