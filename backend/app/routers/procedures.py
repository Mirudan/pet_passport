from datetime import date
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import Procedure, Pet
from app.schemas.procedures import ProcedureResponse, ProcedureCreate

router = APIRouter(prefix="/pets/{pet_id}/procedures", tags=["procedures"])


@router.post("/", response_model=ProcedureResponse, status_code=status.HTTP_201_CREATED)
async def create_procedure(
        pet_id: int,
        procedure_data: ProcedureCreate,
        db: AsyncSession = Depends(get_db)
):
    """
    Создание новой процедуры для питомца.
    - **procedure_type**: Тип процедуры (vaccination/parasite_treatment)
    - **name**: Название процедуры
    - **date_performed**: Дата выполнения
    - **validity_days**: Срок действия в днях
    """
    # Проверяем существование питомца
    pet = await db.get(Pet, pet_id)
    if not pet:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Питомец не найден")

    # Создаем объект процедуры (next_due_date рассчитывается в модели)
    new_procedure = Procedure(
        **procedure_data.model_dump(by_alias=True),  # Учитываем alias 'type'
        pet_id=pet_id
    )

    db.add(new_procedure)
    await db.commit()
    await db.refresh(new_procedure)
    return new_procedure


@router.get("/", response_model=list[ProcedureResponse])
async def get_procedures(
        pet_id: int,
        # Параметры пагинации
        skip: int = Query(0, ge=0, description="Сколько записей пропустить"),
        limit: int = Query(100, le=1000, description="Лимит записей на страницу"),
        # Параметры фильтрации
        start_date: date | None = Query(
            None,
            description="Фильтр: процедуры с этой даты (включительно)"
        ),
        end_date: date | None = Query(
            None,
            description="Фильтр: процедуры до этой даты (включительно)"
        ),
        db: AsyncSession = Depends(get_db)
):
    """
    Получение списка процедур с пагинацией и фильтрацией.
    """
    # Проверяем существование питомца
    pet = await db.get(Pet, pet_id)
    if not pet:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Питомец не найден")

    # Валидация дат
    if start_date and end_date and start_date > end_date:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Дата начала не может быть позже даты окончания"
        )

    # Строим базовый запрос
    query = select(Procedure).where(Procedure.pet_id == pet_id)

    # Добавляем фильтрацию по дате
    if start_date or end_date:
        filters = []
        if start_date:
            filters.append(Procedure.date_performed >= start_date)
        if end_date:
            filters.append(Procedure.date_performed <= end_date)
        query = query.where(and_(*filters))

    # Добавляем сортировку и пагинацию
    query = (
        query.order_by(Procedure.date_performed.desc())
        .offset(skip)
        .limit(limit)
    )

    # Выполняем запрос
    result = await db.execute(query)
    procedures = result.scalars().all()

    return procedures