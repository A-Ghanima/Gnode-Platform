from fastapi import APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends
from app.core.security import verify_password, create_access_token, get_password_hash
from app.core.config import settings
from pydantic import BaseModel

router = APIRouter()

class Token(BaseModel):
    access_token: str
    token_type: str

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    is_valid_user = form_data.username == settings.ADMIN_USERNAME
    is_valid_pass = verify_password(form_data.password, settings.ADMIN_PASSWORD)

    if not is_valid_user or not is_valid_pass:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    token = create_access_token(data={"sub": form_data.username})
    return {"access_token": token, "token_type": "bearer"}
