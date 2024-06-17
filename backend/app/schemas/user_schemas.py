from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserDisplay(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    username: Optional[str]
    password: Optional[str]
    profile_picture_url: Optional[HttpUrl]