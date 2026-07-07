from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from app.services.docker_service import (
    get_all_containers,
    restart_container,
    stop_container,
    start_container,
)
from app.core.security import decode_token
from jose import JWTError

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_token(token)
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.get("/")
async def list_containers(user: str = Depends(get_current_user)):
    return get_all_containers()

@router.post("/{container_id}/restart")
async def restart(container_id: str, user: str = Depends(get_current_user)):
    result = restart_container(container_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Container not found")
    return {"message": f"Container {container_id} restarted"}

@router.post("/{container_id}/stop")
async def stop(container_id: str, user: str = Depends(get_current_user)):
    result = stop_container(container_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Container not found")
    return {"message": f"Container {container_id} stopped"}

@router.post("/{container_id}/start")
async def start(container_id: str, user: str = Depends(get_current_user)):
    result = start_container(container_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Container not found")
    return {"message": f"Container {container_id} started"}
