from sqlalchemy import select
from fastapi import Depends
from apps.users.schemas import UserPatch, UserUpdate
from core.connections import get_session
from core.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from core.security import get_password_hash, verify_password


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, user: User):
        hashed_password = get_password_hash(user.password)
        db_user = User(email=user.email, username=user.username, password=hashed_password)
        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)
        return db_user

    async def get_user_by_email(self, email: str) -> User | None:
        async with self.session:
            result = await self.session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def authenticate_user(self, email: str, password: str) -> User | None:
        user = await self.get_user_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return user

    async def get_users(self, page: int, size: int) -> list[User]:
        async with self.session:
            result = await self.session.execute(select(User).offset((page - 1) * size).limit(size))
        return result.scalars().all()

    async def get_user_by_id(self, user_id: int) -> User | None:
        async with self.session:
            result = await self.session.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_user_by_username(self, username: str) -> User | None:
        async with self.session:
            result = await self.session.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    async def update_user(self, user_id: int, data: UserUpdate) -> User | None:
        async with self.session:
            result = await self.session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if user is None:
            return None
        for key, value in data.model_dump().items():
            if value is not None:
                setattr(user, key, value)
        async with self.session:
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)
        return user

    async def patch_user(self, user_id: int, data: UserPatch) -> User | None:
        async with self.session:
            result = await self.session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if user is None:
            return None
        for key, value in data.model_dump().items():
            if value is not None:
                setattr(user, key, value)
        async with self.session:
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)
        return user

    async def delete_user(self, user_id: int) -> None:
        async with self.session:
            result = await self.session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if user is None:
            return None
        async with self.session:    
            await self.session.delete(user)
            await self.session.commit()

def get_user_service(session: AsyncSession = Depends(get_session)) -> UserService:
    return UserService(session)
