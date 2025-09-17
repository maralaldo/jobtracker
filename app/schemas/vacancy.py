from pydantic import BaseModel
from typing import Optional


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


class VacancyUpdate(BaseModel):
    title: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    salary: Optional[int] = None
    url: Optional[str] = None
    source: Optional[str] = None
