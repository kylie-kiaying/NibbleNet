from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserDisplay(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True
