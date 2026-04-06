from pydantic import BaseModel, EmailStr
from typing import Optional


class UserBase(BaseModel):
    username: str
    email: Optional[EmailStr] = None


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: str
    created_at: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    username: Optional[str] = None