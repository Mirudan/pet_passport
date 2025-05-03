from enum import Enum
from pydantic import BaseModel, Field
from datetime import date
from typing import Optional


class ProcedureType(str, Enum):
    VACCINATION = "vaccination"
    PARASITE_TREATMENT = "parasite_treatment"


class ProcedureBase(BaseModel):
    procedure_type: ProcedureType = Field(..., example=ProcedureType.VACCINATION, alias="type")
    name: str = Field(..., example="Нобивак Rabies", max_length=100)
    date_performed: date = Field(..., example="2024-01-15")
    validity_days: int = Field(..., example=365, gt=0)


class ProcedureCreate(ProcedureBase):
    pass


class ProcedureResponse(ProcedureBase):
    id: int
    pet_id: int
    next_due_date: Optional[date] = Field(example="2025-01-15")

    class Config:
        from_attributes = True
