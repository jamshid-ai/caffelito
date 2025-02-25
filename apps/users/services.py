from sqlalchemy import select
from fastapi import Depends
from apps.users.schemas import UserPatch, UserUpdate
from core.connections import get_session
from core.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from core.security import get_password_hash, verify_password


class UserService:
    """
    Service class to handle operations related to users.
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize the UserService with a database session.

        :param session: An asynchronous database session.
        """
        self.session = session

    async def create_user(self, user: User) -> User:
        """
        Create a new user with a hashed password.

        :param user: The user data to create.
        :return: The created user.
        """
        hashed_password = get_password_hash(user.password)
        db_user = User(email=user.email, username=user.username, password=hashed_password)
        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)
        return db_user

    async def get_user_by_email(self, email: str) -> User | None:
        """
        Retrieve a user by their email.

        :param email: The email of the user to retrieve.
        :return: The user if found, otherwise None.
        """
        async with self.session:
            result = await self.session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def authenticate_user(self, email: str, password: str) -> User | None:
        """
        Authenticate a user by their email and password.

        :param email: The email of the user.
        :param password: The password of the user.
        :return: The user if authentication is successful, otherwise None.
        """
        user = await self.get_user_by_email(email)
        if not user or not verify_password(password, user.password):
            return None
        return user

    async def get_users(self, page: int, size: int) -> list[User]:
        """
        Retrieve a list of users with pagination.

        :param page: The page number to retrieve.
        :param size: The number of users per page.
        :return: A list of users.
        """
        async with self.session:
            result = await self.session.execute(select(User).offset((page - 1) * size).limit(size))
        return result.scalars().all()

    async def get_user_by_id(self, user_id: int) -> User | None:
        """
        Retrieve a user by their ID.

        :param user_id: The ID of the user to retrieve.
        :return: The user if found, otherwise None.
        """
        async with self.session:
            result = await self.session.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_user_by_username(self, username: str) -> User | None:
        """
        Retrieve a user by their username.

        :param username: The username of the user to retrieve.
        :return: The user if found, otherwise None.
        """
        async with self.session:
            result = await self.session.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    async def update_user(self, user_id: int, data: UserUpdate) -> User | None:
        """
        Update a user's information by their ID.

        :param user_id: The ID of the user to update.
        :param data: The updated user data.
        :return: The updated user if found, otherwise None.
        """
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
        """
        Partially update a user's information by their ID.

        :param user_id: The ID of the user to patch.
        :param data: The partial user data to update.
        :return: The updated user if found, otherwise None.
        """
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
        """
        Delete a user by their ID.

        :param user_id: The ID of the user to delete.
        """
        async with self.session:
            result = await self.session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if user is None:
            return None
        async with self.session:    
            await self.session.delete(user)
            await self.session.commit()

def get_user_service(session: AsyncSession = Depends(get_session)) -> UserService:
    """
    Dependency to get a UserService instance with a session.

    :param session: An asynchronous database session.
    :return: A UserService instance.
    """
    return UserService(session)
