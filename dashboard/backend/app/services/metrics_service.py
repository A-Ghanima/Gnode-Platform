import httpx
import docker
import concurrent.futures
from app.core.config import settings

client = docker.from_env()

def get_container_stats(container_name: str) -> dict:
    try:
        container = client.containers.get(container_name)
        stats = container.stats(stream=False)
        cpu_delta = stats["cpu_stats"]["cpu_usage"]["total_usage"] - \
                    stats["precpu_stats"]["cpu_usage"]["total_usage"]
        system_delta = stats["cpu_stats"]["system_cpu_usage"] - \
                       stats["precpu_stats"]["system_cpu_usage"]
        num_cpus = stats["cpu_stats"].get("online_cpus", 1)
        cpu_percent = (cpu_delta / system_delta) * num_cpus * 100 if system_delta > 0 else 0.0
        mem_usage = stats["memory_stats"].get("usage", 0)
        mem_limit = stats["memory_stats"].get("limit", 1)
        mem_mb = round(mem_usage / (1024 * 1024), 2)
        mem_percent = round((mem_usage / mem_limit) * 100, 2) if mem_limit > 0 else 0.0
        return {"cpu_percent": round(cpu_percent, 2), "ram_mb": mem_mb, "ram_percent": mem_percent}
    except Exception:
        return {"cpu_percent": 0.0, "ram_mb": 0.0, "ram_percent": 0.0}

def get_all_container_stats(names: list) -> dict:
    result = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(get_container_stats, name): name for name in names}
        for future in concurrent.futures.as_completed(futures):
            name = futures[future]
            result[name] = future.result()
    return result

async def query_prometheus(query: str) -> dict:
    async with httpx.AsyncClient() as client:
        res = await client.get(
            f"{settings.PROMETHEUS_URL}/api/v1/query",
            params={"query": query},
            timeout=10
        )
        res.raise_for_status()
        return res.json()

async def get_host_metrics() -> dict:
    cpu_query = '100 - (avg(rate(node_cpu_seconds_total{mode="idle"}[2m])) * 100)'
    ram_query = '(1 - node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes) * 100'
    disk_query = '(node_filesystem_size_bytes{mountpoint="/"} - node_filesystem_free_bytes{mountpoint="/"}) / node_filesystem_size_bytes{mountpoint="/"} * 100'
    cpu_data = await query_prometheus(cpu_query)
    ram_data = await query_prometheus(ram_query)
    disk_data = await query_prometheus(disk_query)
    def extract(data):
        results = data.get("data", {}).get("result", [])
        if results:
            return round(float(results[0]["value"][1]), 2)
        return 0.0
    return {"cpu_percent": extract(cpu_data), "ram_percent": extract(ram_data), "disk_percent": extract(disk_data)}
