from typing import Optional, AsyncGenerator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.security import decode_token
from app.repositories.user_repo import UserRepository
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)

async def get_current_user(
    db: AsyncSession = Depends(get_db),
    token: Optional[str] = Depends(oauth2_scheme)
) -> Optional[User]:
    if not token:
        return None
    payload = decode_token(token)
    if not payload:
        return None
    user_id = payload.get("sub")
    if not user_id:
        return None
    user_repo = UserRepository(db)
    user = await user_repo.get_by_id(user_id)
    return user

async def get_current_active_user(
    current_user: Optional[User] = Depends(get_current_user)
) -> User:
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def require_role(required_role: str):
    async def role_checker(current_user: User = Depends(get_current_active_user)) -> User:
        user_roles = [r.name for r in current_user.roles]
        if "SUPER_ADMIN" in user_roles or required_role in user_roles:
            return current_user
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User lacks required role: {required_role}"
        )
    return role_checker
