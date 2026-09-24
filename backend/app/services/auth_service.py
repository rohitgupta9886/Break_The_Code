from typing import Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.repositories.user_repo import UserRepository
from app.models.user import User, Role
from app.schemas.user import UserCreate, UserLogin, UserRead
from app.core.security import verify_password, get_password_hash, create_access_token

class AuthService:
    def __init__(self, session: AsyncSession):
        self.user_repo = UserRepository(session)

    async def register(self, user_in: UserCreate) -> Tuple[User, str]:
        existing = await self.user_repo.get_by_email(user_in.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists"
            )

        hashed_pw = get_password_hash(user_in.password)
        user = User(
            email=user_in.email.lower().strip(),
            hashed_password=hashed_pw,
            full_name=user_in.full_name,
            avatar_url=user_in.avatar_url,
            is_active=True,
            is_verified=True
        )

        # Assign default USER role
        user_role = await self.user_repo.get_role_by_name("USER")
        if user_role:
            user.roles.append(user_role)

        created_user = await self.user_repo.create(user)
        token = create_access_token(
            subject=created_user.id,
            role="USER"
        )
        return created_user, token

    async def login(self, login_in: UserLogin) -> Tuple[User, str]:
        user = await self.user_repo.get_by_email(login_in.email)
        if not user or not verify_password(login_in.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is deactivated"
            )

        # Record login timestamp
        from datetime import datetime, timezone
        user.last_active_date = datetime.now(timezone.utc)
        await self.user_repo.session.commit()

        primary_role = user.roles[0].name if user.roles else "USER"
        token = create_access_token(subject=user.id, role=primary_role)
        return user, token
