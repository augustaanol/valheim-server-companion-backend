import httpx
import asyncio
import logging
from app.config import VALHEIM_HOST_IP, VALHEIM_STATUS_PORT, THUNDERSTORE_API

# Konfiguracja logowania


async def extract_mods() -> list[dict]:
    url = f"http://{VALHEIM_HOST_IP}:{VALHEIM_STATUS_PORT}/status"
    async with httpx.AsyncClient(timeout=5.0) as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            return data.get("bepinex", {}).get("mods", [])
        except Exception as e:
            logger.error(f"Błąd BepInEx: {e}")
            return []


import httpx
import asyncio
import logging
from app.config import VALHEIM_HOST_IP, VALHEIM_STATUS_PORT, THUNDERSTORE_API

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def normalize(text: str) -> str:
    if not text:
        return ""
    return (
        text.lower()
        .replace(".dll", "")
        .replace("_", "")
        .replace("-", "")
        .replace(" ", "")
        .replace(".", "")
    )


async def fetch_thunderstore_packages() -> list:
    logger.info(f"Pobieranie bazy z {THUNDERSTORE_API}...")
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            response = await client.get(THUNDERSTORE_API)
            data = response.json()
            # Thunderstore API V1 zwraca LISTĘ bezpośrednio, nie słownik z 'results'
            packages = data if isinstance(data, list) else data.get("results", [])
            logger.info(f"Pobrano {len(packages)} paczek.")
            return packages
        except Exception as e:
            logger.error(f"Błąd API Thunderstore: {e}")
            return []


def create_smart_index(packages: list) -> dict:
    """
    Kluczowy krok: Indeksujemy każdą możliwą nazwę, którą może mieć DLL.
    """
    index = {}
    for pkg in packages:
        # full_name to np. "Azumatt-AzuAutoStore"
        full_name = pkg.get("full_name", "")
        # name to np. "AzuAutoStore"
        name = pkg.get("name", "")

        # Normalizujemy oba warianty
        norm_full = normalize(full_name)
        norm_name = normalize(name)

        # Zapisujemy w indeksie
        if norm_full:
            index[norm_full] = pkg
        if norm_name:
            index[norm_name] = pkg

        # Dodatkowo: niektóre DLL używają spacji, których TS nie ma w 'name'
        # ale ma w nazwach wersji. Tutaj to pomijamy dla wydajności.
    return index


async def enrich_mods() -> list[dict]:
    # Pobieranie statusu serwera
    url = f"http://{VALHEIM_HOST_IP}:{VALHEIM_STATUS_PORT}/status"

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            resp = await client.get(url)
            server_data = resp.json()
            server_mods = server_data.get("bepinex", {}).get("mods", [])
        except Exception as e:
            logger.error(f"Błąd serwera Valheim: {e}")
            return []

    ts_packages = await fetch_thunderstore_packages()
    ts_index = create_smart_index(ts_packages)

    enriched = []
    for mod in server_mods:
        raw_name = mod.get("name", "")
        clean_name = normalize(raw_name)

        match = None
        # 1. Szukaj po pełnej nazwie (np. azuautostore)
        if clean_name in ts_index:
            match = ts_index[clean_name]

        # 2. Szukaj po nazwie bez autora (jeśli w DLL jest "Azumatt_AzuAutoStore")
        if not match and "_" in raw_name:
            suffix = normalize(raw_name.split("_")[-1])
            match = ts_index.get(suffix)

        if match:
            # W TS API V1 wersje są w liście 'versions', najnowsza to zazwyczaj index 0
            versions = match.get("versions", [])
            latest = versions[0] if versions else {}

            enriched.append(
                {
                    "dll_name": raw_name,
                    "matched": True,
                    "mod_name": match.get("name"),
                    "author": match.get("owner"),
                    "latest_version": latest.get("version_number"),
                    "url": match.get("package_url")
                    or f"https://thunderstore.io/package/{match.get('owner')}/{match.get('name')}/",
                    "download_url": latest.get("download_url"),
                }
            )
        else:
            enriched.append({"dll_name": raw_name, "matched": False})

    return enriched
