from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import Pet, User
from app.schemas.pets import PetCreate, PetResponse, PetsListResponse

router = APIRouter(prefix="/pets", tags=["pets"])


@router.post("/", response_model=PetResponse, status_code=201)
async def create_pet(
        pet: PetCreate,
        owner_id: int,  # Идентификатор владельца из запроса
        db: AsyncSession = Depends(get_db)
):
    # Проверяем, существует ли владелец
    owner = await db.execute(select(User).where(User.id == owner_id))
    owner = owner.scalar()
    if not owner:
        raise HTTPException(404, "Owner not found")

    # Проверяем, не превышен ли лимит питомцев
    if len(owner.pets) >= 5:
        raise HTTPException(400, "Maximum 5 pets per user")

    # Создаем питомца
    new_pet = Pet(**pet.model_dump(), owner_id=owner_id)
    db.add(new_pet)
    await db.commit()
    await db.refresh(new_pet)
    return new_pet


@router.get("/{pet_id}", response_model=PetResponse)
async def get_pet(pet_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Pet).where(Pet.id == pet_id))
    pet = result.scalar()
    if not pet:
        raise HTTPException(404, "Pet not found")
    return pet


@router.delete("/{pet_id}", status_code=204)
async def delete_pet(pet_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Pet).where(Pet.id == pet_id))
    pet = result.scalar()
    if not pet:
        raise HTTPException(404, "Pet not found")

    await db.delete(pet)
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get("/", response_model=PetsListResponse)
async def get_all_pets(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,  # Пагинация: пропустить первые N записей
    limit: int = 100  # Лимит записей на страницу
):
    result = await db.execute(select(Pet).offset(skip).limit(limit))
    pets = result.scalars().all()
    return {"items": pets}