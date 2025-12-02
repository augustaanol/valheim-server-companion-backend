import docker

client = docker.DockerClient(base_url="unix://var/run/docker.sock")


def get_container_resources(container_name: str):
    try:
        container = client.containers.get(container_name)
        stats = container.stats(stream=False)

        # CPU calculation
        cpu_total = stats["cpu_stats"]["cpu_usage"]["total_usage"]
        cpu_system = stats["cpu_stats"].get("system_cpu_usage", 0)
        cpu_percent = (cpu_total / cpu_system) * 100 if cpu_system > 0 else 0

        # Memory calculation
        mem_usage = stats["memory_stats"]["usage"]
        mem_limit = stats["memory_stats"].get("limit", 1)
        mem_percent = (mem_usage / mem_limit) * 100

        return {
            "cpu_percent": round(cpu_percent, 2),
            "memory_usage": mem_usage,
            "memory_limit": mem_limit,
            "memory_percent": round(mem_percent, 2),
        }

    except Exception as e:
        return {"error": str(e)}
