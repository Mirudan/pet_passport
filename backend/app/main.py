from fastapi import FastAPI
from app.routers import users, pets, procedures, weight

# Создаем экземпляр FastAPI приложения
app = FastAPI(
    title="Pet Passport API",
    description="API для управления паспортами питомцев",
    version="0.1.0"
)

# Подключаем роутер с пользовательскими эндпоинтами
app.include_router(users.router)
app.include_router(pets.router)
app.include_router(procedures.router)
app.include_router(weight.router)

# Простейший тестовый эндпоинт для проверки работы
@app.get("/", tags=["Healthcheck"])
async def root():
    return {
        "message": "Pet Passport API работает!",
        "documentation": "/docs или /redoc"
    }