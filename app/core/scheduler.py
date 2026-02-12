from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.ext.asyncio import async_sessionmaker
from app.db.session import engine
from app.services.thunderstore_service import refresh_thunderstore_cache
from app.services.server_mod_service import refresh_server_mods
import logging

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()

# tworzymy session factory
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def daily_mod_sync():
    logger.info("Starting daily mod sync...")
    async with async_session() as db:
        await refresh_thunderstore_cache(db)
        await refresh_server_mods(db)
    logger.info("Daily mod sync finished.")


def start_scheduler():
    scheduler.add_job(daily_mod_sync, "interval", hours=24)
    scheduler.start()