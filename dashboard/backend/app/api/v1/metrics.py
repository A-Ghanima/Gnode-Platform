from fastapi import APIRouter, Depends, HTTPException
from app.api.v1.containers import get_current_user
from app.services.metrics_service import get_host_metrics, get_container_stats, get_all_container_stats
from app.services.docker_service import get_all_containers

router = APIRouter()

@router.get("/host")
async def host_metrics(user: str = Depends(get_current_user)):
    try:
        return await get_host_metrics()
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Prometheus unavailable: {str(e)}")

@router.get("/container/{name}")
async def container_metrics(name: str, user: str = Depends(get_current_user)):
    return get_container_stats(name)

@router.get("/containers")
async def all_container_metrics(user: str = Depends(get_current_user)):
    containers = get_all_containers()
    names = [c["name"] for c in containers if c["status"] == "running"]
    return get_all_container_stats(names)
