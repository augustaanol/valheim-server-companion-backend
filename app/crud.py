from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app import models, schemas


async def create_log(session: AsyncSession, log: schemas.PlayerLogCreate):
    db_log = models.PlayerLog(**log.dict())
    session.add(db_log)
    await session.commit()
    await session.refresh(db_log)
    return db_log


async def get_logs(session: AsyncSession, limit: int = 100):
    result = await session.execute(select(models.PlayerLog).limit(limit))
    return result.scalars().all()
