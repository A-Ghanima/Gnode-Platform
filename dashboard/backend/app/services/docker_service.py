import docker
from docker.errors import NotFound
from typing import List, Dict, Any

client = docker.from_env()

def get_all_containers() -> List[Dict[str, Any]]:
    containers = client.containers.list(all=True)
    result = []
    for c in containers:
        result.append({
            "id": c.short_id,
            "name": c.name,
            "status": c.status,
            "image": c.image.tags[0] if c.image.tags else "unknown",
            "created": c.attrs["Created"],
            "group": c.labels.get("gnode.group", "other"),
        })
    return result

def restart_container(container_id: str) -> bool:
    try:
        container = client.containers.get(container_id)
        container.restart()
        return True
    except NotFound:
        return None

def stop_container(container_id: str) -> bool:
    try:
        container = client.containers.get(container_id)
        container.stop()
        return True
    except NotFound:
        return None

def start_container(container_id: str) -> bool:
    try:
        container = client.containers.get(container_id)
        container.start()
        return True
    except NotFound:
        return None
