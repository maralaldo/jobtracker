from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from app.core.security import get_current_user
from app.crud import users
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.models.user import User as UserModel

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserRead)
async def create_user(user_in: UserCreate, db: AsyncSession = Depends(get_session)):
    return await users.create_user(db=db, user=user_in)


@router.get("/me", response_model=UserRead)
async def read_users_me(current_user: UserModel = Depends(get_current_user)):
    return current_user


@router.get("/", response_model=list[UserRead])
async def list_users(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_session)):
    return await users.get_users(db=db, skip=skip, limit=limit)


@router.get("/{user_id}", response_model=UserRead)
async def read_user(user_id: int, db: AsyncSession = Depends(get_session)):
    db_user = await users.get_user(db=db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.patch("/{user_id}", response_model=UserRead)
async def update_user(user_id: int, user_update: UserUpdate, db: AsyncSession = Depends(get_session)):
    db_user = await users.update_user(db, user_id, user_update)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_session)):
    ok = await users.delete_user(db, user_id)
    if not ok:
        raise HTTPException(status_code=404, detail="User not found")
    return Response(status_code=204)
