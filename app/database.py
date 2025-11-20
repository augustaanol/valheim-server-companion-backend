from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

POSTGRES_USER = "valheim"
POSTGRES_PASSWORD = "xyz123"
POSTGRES_DB = "valheim_logs"
POSTGRES_HOST = "10.0.0.5"  # IP TrueNAS / hostname kontenera PostgreSQL
POSTGRES_PORT = 5432

DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
