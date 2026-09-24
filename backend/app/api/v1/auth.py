from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.services.auth_service import AuthService
from app.schemas.user import UserCreate, UserLogin, UserRead, TokenResponse

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    service = AuthService(db)
    user, token = await service.register(user_in)
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user=UserRead.model_validate(user)
    )

@router.post("/login", response_model=TokenResponse)
async def login(
    login_in: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    service = AuthService(db)
    user, token = await service.login(login_in)
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user=UserRead.model_validate(user)
    )
