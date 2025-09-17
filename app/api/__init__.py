from fastapi import APIRouter
from app.api import auth, users, vacancies, filters

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(vacancies.router)
api_router.include_router(filters.router)
