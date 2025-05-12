"""
Файл содержит описание моделей БД
"""
import datetime
from typing import Optional

from pydantic_core.core_schema import ValidationInfo
from sqlmodel import SQLModel, Field
from pydantic import EmailStr, field_validator


class User(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    username: str = Field(index=True)
    password: str = Field(max_length=256, min_length=6)
    email: EmailStr
    created_at: datetime.datetime = datetime.datetime.now()


class UserInput(SQLModel):
    username: str
    password: str = Field(max_length=256, min_length=6)
    password2: str = Field(max_length=256, min_length=6)
    email: EmailStr

    @field_validator('password2')
    def password_match(cls, v: str, info: ValidationInfo) -> str:
        if "password1" in info.data and v != info.data["password1"]:
            raise ValueError("Пароли отличаются!")
        return v


class UserLogin(SQLModel):
    username: str
    password: str = Field(max_length=256, min_length=6)