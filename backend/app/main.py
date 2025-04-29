from fastapi import FastAPI
from .database import engine, Base
from contextlib import \
    asynccontextmanager  # декоратор для создания асинхронного контекстного менеджера (управляет жизненным циклом приложения)


# Создаем таблицы БД при старте приложения для теста
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}