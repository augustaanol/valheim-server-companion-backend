from fastapi import FastAPI
from app.api.endpoints import (
    server_status,
    container_control,
    rcon,
    server_stats,
    teleport,
)
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Valheim Companion API")

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
app.include_router(server_status.router, prefix="/api")
app.include_router(container_control.router, prefix="/api")
app.include_router(rcon.router, prefix="/api")
app.include_router(server_stats.router, prefix="/api")
app.include_router(teleport.router, prefix="/api")
