from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from os import getenv
from dotenv import load_dotenv

load_dotenv()  # Загружаем переменные из .env

# Настройки подключения к PostgreSQL
# Формат URL: postgresql+asyncpg://user:password@host:port/db_name
POSTGRES_URL = (
    f"postgresql+asyncpg://{getenv('POSTGRES_USER')}:{getenv('POSTGRES_PASSWORD')}"
    f"@{getenv('POSTGRES_HOST')}:{getenv('POSTGRES_PORT')}/{getenv('POSTGRES_DB')}"
)

engine = create_async_engine(POSTGRES_URL, echo=True)  # echo=True для логирования SQL
Base = declarative_base()

# Асинхронная сессия для работы с БД
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)
