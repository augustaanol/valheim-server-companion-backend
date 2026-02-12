from fastapi import FastAPI
from app.api.endpoints import (
    mods_api,
    rcon_api,
    server_stats_api,
    container_control_api,
    server_status_api,
    teleport_api,
    container_resources_api,
    players_api,
    tasks_api,
    comments_api,
    task_events_api,
)
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio

from app.services.player_sync import sync_players_loop

from app.core.scheduler import start_scheduler, daily_mod_sync

import os
print("APP DATABASE_URL =", os.getenv("DATABASE_URL"))

@asynccontextmanager
async def lifespan(app: FastAPI):
    # STARTUP
    task = asyncio.create_task(sync_players_loop())

    await daily_mod_sync()

    # 🔁 scheduler co 24h
    start_scheduler()
    
    yield  # <- aplikacja działa

    # SHUTDOWN
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass


app = FastAPI(title="Valheim Companion API", lifespan=lifespan)

# ----------------------------
# Konfiguracja CORS
# ----------------------------
# allow_origins = ["http://localhost:3000"]  -> dev Next.js
# lub ["*"] jeśli chcesz otworzyć na wszystkie źródła (prywatne Tailscale)
origins = [
    "http://localhost:3000",  # Next.js dev
    "http://127.0.0.1:3000",
    "http://100.96.243.7:3000",
    "http://192.168.200.113:3000",
    "http://backend:3000",
    "http://backend",
    "http://frontend:3000",
    "http://frontend",
    "*",  # w produkcji Tailscale możesz zostawić *
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rejestracja routerów
app.include_router(server_status_api.router, prefix="/api")
app.include_router(container_control_api.router, prefix="/api")
app.include_router(rcon_api.router, prefix="/api")
app.include_router(server_stats_api.router, prefix="/api")
app.include_router(teleport_api.router, prefix="/api")
app.include_router(container_resources_api.router, prefix="/api")
app.include_router(players_api.router, prefix="/api")
app.include_router(tasks_api.router, prefix="/api")
app.include_router(comments_api.router, prefix="/api")
app.include_router(task_events_api.router, prefix="/api")
app.include_router(mods_api.router, prefix="/api")
