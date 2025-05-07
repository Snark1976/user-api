import re
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, field_validator, ConfigDict


class UserDTO(BaseModel):
    id: UUID
    name: str
    surname: str
    password: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )

class UserUpdateDTO(BaseModel):
    name: str | None = Field(default=None, description="Updated name")
    surname: str | None = Field(default=None, description="Updated surname")
    password: str | None = Field(default=None, description="Updated password")

class UserCreateDTO(BaseModel):
    name: str = Field(..., min_length=1)
    surname: str = Field(..., min_length=1)
    password: str

    @field_validator('password')
    def validate_password(cls, v: str) -> str:
        errors = []
        if len(v) < 8:
            errors.append("минимум 8 символов")
        if not re.search(r"[A-Z]", v):
            errors.append("хотя бы одна заглавная буква")
        if not re.search(r"[a-z]", v):
            errors.append("хотя бы одна строчная буква")
        if not re.search(r"\d", v):
            errors.append("хотя бы одна цифра")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            errors.append("хотя бы один специальный символ")

        if errors:
            raise ValueError(f"Пароль должен содержать: {', '.join(errors)}")
        return v