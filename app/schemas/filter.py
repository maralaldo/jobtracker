from pydantic import BaseModel
from typing import Optional


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


class FilterUpdate(BaseModel):
    keyword: Optional[str] = None
    location: Optional[str] = None
    min_salary: Optional[int] = None
    max_salary: Optional[int] = None
