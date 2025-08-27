from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    telegram_id: Optional[str] = None


class UserRead(BaseModel):
    id: int
    name: str
    email: EmailStr
    telegram_id: Optional[str] = None

    class Config:
        from_attributes = True
