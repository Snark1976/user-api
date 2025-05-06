from datetime import datetime
from uuid import UUID

from litestar.dto import DTOData
from pydantic import BaseModel, Field

class UserDTO(BaseModel):
    id: UUID
    name: str
    surname: str
    password: str
    created: datetime
    updated: datetime

    class Config:
        from_attributes = True

class UserUpdateDTO(BaseModel):
    name: str | None = Field(default=None, description="Updated name")
    surname: str | None = Field(default=None, description="Updated surname")
    password: str | None = Field(default=None, description="Updated password")

class UserCreateDTO(BaseModel):
    name: str
    surname: str
    password: str