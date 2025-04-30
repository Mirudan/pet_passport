from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import User
from app.schemas.users import UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    # Проверяем, есть ли пользователь в БД
    existing_user = await db.execute(User).where(User.telegram_id == user.telegram_id)
    if existing_user.scalar():
        raise HTTPException(400, "User already exists")

    # Создаем нового пользователя
    new_user = User(**user.model_dump())
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


@router.get("/{telegram_id}", response_model=UserResponse)
async def get_user(telegram_id: int, db: AsyncSession = Depends(get_db)):
    user = await db.execute(User).where(User.telegram_id == telegram_id)
    user = user.scalar()
    if not user:
        raise HTTPException(404, "User not found")
    return user
