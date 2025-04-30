from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from os import getenv
from dotenv import load_dotenv

load_dotenv()

# Настройка подключения к PostgreSQL
POSTGRES_URL = (
    f"postgresql+asyncpg://{getenv('POSTGRES_USER')}:{getenv('POSTGRES_PASSWORD')}"
    f"@{getenv('POSTGRES_HOST')}:{getenv('POSTGRES_PORT')}/{getenv('POSTGRES_DB')}"
)

# Асинхронный движок
engine = create_async_engine(POSTGRES_URL, echo=True)

# Базовый класс для моделей
Base = declarative_base()

# Фабрика асинхронных сессий
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)


# Генератор сессий для зависимостей
async def get_db() -> AsyncSession:
    """
    Генерирует асинхронную сессию БД для каждого запроса.
    Автоматически закрывает сессию после завершения.
    """
    async with AsyncSessionLocal() as session:
        yield session
