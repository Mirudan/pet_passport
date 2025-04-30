from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from os import getenv
from dotenv import load_dotenv

load_dotenv()  # Загружаем переменные из .env

# Настройки подключения к PostgreSQL
# Формат URL: postgresql+asyncpg://user:password@host:port/db_name
SQLALCHEMY_DATABASE_URL = (getenv("SQLALCHEMY_DATABASE_URL"))

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)  # echo=True для логирования SQL
Base = declarative_base()

# Асинхронная сессия для работы с БД
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)
