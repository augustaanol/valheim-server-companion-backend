from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.database import engine
from app.models import Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting FastAPI + PostgreSQL…")

    # Utworzenie modeli przy starcie
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    print("Shutting down…")
    await engine.dispose()

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"status": "ok"}