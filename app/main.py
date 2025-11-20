from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app import database, crud, schemas, models

app = FastAPI(title="Valheim Companion API")


# create tables on startup
@app.on_event("startup")
async def startup():
    async with database.engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


@app.post("/logs/", response_model=schemas.PlayerLogCreate)
async def add_log(
    log: schemas.PlayerLogCreate, session: AsyncSession = Depends(database.get_session)
):
    return await crud.create_log(session, log)


@app.get("/logs/")
async def read_logs(
    limit: int = 100, session: AsyncSession = Depends(database.get_session)
):
    return await crud.get_logs(session, limit)
