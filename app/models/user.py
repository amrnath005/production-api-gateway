from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=100)
    email: EmailStr
    password: str | None = Field(default=None, min_length=6)
    role: str = Field(default="user", max_length=50)
    age: int = Field(ge=0, le=150)


class UserUpdate(BaseModel):
    username: str | None = Field(default=None, min_length=3, max_length=100)
    email: EmailStr | None = None
    password: str | None = Field(default=None, min_length=6)
    role: str | None = Field(default=None, max_length=50)
    age: int | None = Field(default=None, ge=0, le=150)
    is_active: bool | None = None


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: EmailStr
    role: str = "user"
    age: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
