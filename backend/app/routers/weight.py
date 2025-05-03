from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import WeightRecord, Pet
from app.schemas.weight import WeightCreate, WeightResponse

router = APIRouter(prefix="/pets/{pet_id}/weight", tags=["weight"])


@router.post("/", response_model=WeightResponse, status_code=201)
async def add_weight(
        pet_id: int,
        weight_data: WeightCreate,
        db: AsyncSession = Depends(get_db)
):
    # Проверяем существование питомца
    pet = await db.get(Pet, pet_id)
    if not pet:
        raise HTTPException(404, "Питомец не найден")

    # Удаляем старую запись, если их уже 5
    if len(pet.weight_history) >= 5:
        oldest = pet.weight_history[0]
        await db.delete(oldest)

    # Добавляем новую запись
    new_weight = WeightRecord(**weight_data.model_dump(), pet_id=pet_id)
    db.add(new_weight)
    await db.commit()
    await db.refresh(new_weight)
    return new_weight


@router.get("/", response_model=list[WeightResponse])
async def get_weight_history(
        pet_id: int,
        db: AsyncSession = Depends(get_db)
):
    # Проверяем существование питомца
    pet = await db.get(Pet, pet_id)
    if not pet:
        raise HTTPException(404, "Питомец не найден")

    # Возвращаем все записи веса, отсортированные по дате
    return pet.weight_history
