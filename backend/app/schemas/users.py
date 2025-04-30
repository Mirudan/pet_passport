from pydantic import BaseModel

class UserCreate(BaseModel):
    telegram_id: int
    full_name: str | None = None
    username: str | None = None

class UserResponse(BaseModel):
    id: int
    telegram_id: int
    full_name: str | None
    username: str | None

    class Config:
        from_attributes = True # Конвертирует ORM-объект в Pydantic-модель