import os
import docker

# ============================
# Tryb DEVELOPMENT (bez Dockera)
# ============================

# Odczyt zmiennej z .env lub środowiska
DISABLE_DOCKER = os.environ.get("DISABLE_DOCKER", "false").lower() == "true"

client = None

if DISABLE_DOCKER:
    print("⚠️ Docker disabled by DISABLE_DOCKER=true")
else:
    # Sprawdź czy Docker socket istnieje
    if os.path.exists("/var/run/docker.sock"):
        try:
            client = docker.DockerClient(base_url="unix://var/run/docker.sock")
            print("🐳 Docker client initialized")
        except Exception as e:
            print("⚠️ Could not connect to Docker:", e)
            client = None
    else:
        print("⚠️ Docker socket not found — running in DEV mode")
        DISABLE_DOCKER = True


# ============================
# API
# ============================


def get_container_resources(container_name: str):
    # DEV mode → zwracamy mock zamiast błędu
    if DISABLE_DOCKER or client is None:
        return {
            "cpu_percent": 0,
            "memory_usage": 0,
            "memory_limit": 0,
            "memory_percent": 0,
            "disabled": True,
            "message": "Docker disabled (DISABLE_DOCKER=true or no docker.sock)",
        }

    # TRYB PRODUKCYJNY
    try:
        container = client.containers.get(container_name)
        stats = container.stats(stream=False)

        # CPU calculation
        cpu_total = stats["cpu_stats"]["cpu_usage"]["total_usage"]
        cpu_system = stats["cpu_stats"].get("system_cpu_usage", 0)
        cpu_percent = (cpu_total / cpu_system * 100) if cpu_system > 0 else 0

        # Memory calculation
        mem_usage = stats["memory_stats"]["usage"]
        mem_limit = stats["memory_stats"].get("limit", 1)
        mem_percent = mem_usage / mem_limit * 100

        return {
            "cpu_percent": round(cpu_percent, 2),
            "memory_usage": mem_usage,
            "memory_limit": mem_limit,
            "memory_percent": round(mem_percent, 2),
        }

    except Exception as e:
        return {"error": str(e)}
