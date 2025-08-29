from pydantic import BaseModel, EmailStr
from typing import Optional


# User Schemas
class UserBase(BaseModel):
    name: str
    email: EmailStr
    telegram_id: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    telegram_id: Optional[str] = None
    password: Optional[str] = None


# Vacancy Schemas
class VacancyBase(BaseModel):
    title: str
    company: str
    location: Optional[str] = None
    salary: Optional[int] = None
    url: str
    source: str


class VacancyCreate(VacancyBase):
    pass


class VacancyRead(VacancyBase):
    id: int

    class Config:
        from_attributes = True


# Filter Schemas
class FilterBase(BaseModel):
    keyword: str
    location: Optional[str] = None
    min_salary: Optional[int] = None
    max_salary: Optional[int] = None


class FilterCreate(FilterBase):
    user_id: int


class FilterRead(FilterBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
