from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import User
from app.schemas.users import UserCreate, UserResponse
from sqlalchemy import select

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    # Проверяем, есть ли пользователь в БД
    result = await db.execute(select(User).where(User.telegram_id == user.telegram_id))
    existing_user = result.scalar()

    if existing_user:
        raise HTTPException(400, "User already exists")

    # Создаем нового пользователя
    new_user = User(**user.model_dump())
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


@router.get("/{telegram_id}", response_model=UserResponse)
async def get_user(telegram_id: int, db: AsyncSession = Depends(get_db)):
    user = await db.execute(select(User).where(User.telegram_id == telegram_id))
    user = user.scalar()
    if not user:
        raise HTTPException(404, "User not found")
    return user


@router.get("/", response_model=list[UserResponse])
async def get_all_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users


@router.delete("/{telegram_id}")
async def delete_user(telegram_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.telegram_id == telegram_id))
    user = result.scalar()
    if not user:
        raise HTTPException(404, "User not found")

    await db.delete(user)
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
