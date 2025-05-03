from pydantic import BaseModel, Field
from datetime import date


class WeightBase(BaseModel):
    measurement_date: date = Field(..., example="2024-01-15")
    weight_kg: float = Field(..., example=4.5, gt=0)


class WeightCreate(WeightBase):
    pass


class WeightResponse(WeightBase):
    id: int
    pet_id: int

    class Config:
        from_attributes = True
