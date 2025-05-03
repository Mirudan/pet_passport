from pydantic import BaseModel, Field
from datetime import date
from typing import List


class PetBase(BaseModel):
    name: str = Field(..., max_length=100)
    animal_type: str = Field(..., max_length=50)
    birth_date: date


class PetCreate(PetBase):
    pass


class PetResponse(PetBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True  # Конвертирует ORM-объект в Pydantic


class PetsListResponse(BaseModel):
    items: List[PetResponse]
