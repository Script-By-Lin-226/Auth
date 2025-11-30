from fastapi import HTTPException
from pydantic import BaseModel, EmailStr,validator

class UserBase(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str
    @validator('role')
    def validate_role(cls, value):
        if value not in ['admin', 'user']:
            raise HTTPException(status_code=401, detail="Not authenticated")
        return value


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class PostBase(BaseModel):
    title: str
    content: str

class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    role: str | None = None