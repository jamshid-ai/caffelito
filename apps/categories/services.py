from fastapi import Depends
from sqlalchemy import select
from apps.categories.schemas import CategoryCreate, CategoryRead, CategoryUpdate, CategoryPatch
from core.connections import get_session
from core.models import Category
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List


class CategoryService:
    """
    Service class to handle operations related to categories.
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize the CategoryService with a database session.

        :param session: An asynchronous database session.
        """
        self.session = session

    async def create_category(self, category: CategoryCreate) -> CategoryRead:
        """
        Create a new category.

        :param category: The category data to create.
        :return: The created category.
        """
        async with self.session:
            self.session.add(category)
            await self.session.commit()
            await self.session.refresh(category)
        return category

    async def get_categories(self, page: int, size: int) -> List[CategoryRead]:
        """
        Retrieve a list of categories with pagination.

        :param page: The page number to retrieve.
        :param size: The number of categories per page.
        :return: A list of categories.
        """
        async with self.session:
            result = await self.session.execute(select(Category).offset((page - 1) * size).limit(size))
        return result.scalars().all()

    async def get_category_by_id(self, category_id: int) -> CategoryRead | None:
        """
        Retrieve a category by its ID.

        :param category_id: The ID of the category to retrieve.
        :return: The category if found, otherwise None.
        """
        async with self.session:
            result = await self.session.execute(select(Category).where(Category.id == category_id))
        return result.scalar_one_or_none()

    async def update_category(self, category_id: int, data: CategoryUpdate) -> CategoryRead | None:
        """
        Update a category by its ID.

        :param category_id: The ID of the category to update.
        :param data: The updated category data.
        :return: The updated category if found, otherwise None.
        """
        async with self.session:
            result = await self.session.execute(select(Category).where(Category.id == category_id))
        category = result.scalar_one_or_none()
        if category is None:
            return None
        for key, value in data.model_dump().items():
            if value is not None:
                setattr(category, key, value)
        async with self.session:
            self.session.add(category)
            await self.session.commit()
            await self.session.refresh(category)
        return category

    async def patch_category(self, category_id: int, data: CategoryPatch) -> CategoryRead | None:
        """
        Partially update a category by its ID.

        :param category_id: The ID of the category to patch.
        :param data: The partial category data to update.
        :return: The updated category if found, otherwise None.
        """
        async with self.session:
            result = await self.session.execute(select(Category).where(Category.id == category_id))
        category = result.scalar_one_or_none()
        if category is None:
            return None
        for key, value in data.model_dump().items():    
            if value is not None:
                setattr(category, key, value)
        async with self.session:
            self.session.add(category)
            await self.session.commit()
            await self.session.refresh(category)
        return category 
    
    async def delete_category(self, category_id: int) -> None:
        """
        Delete a category by its ID.

        :param category_id: The ID of the category to delete.
        """
        async with self.session:
            result = await self.session.execute(select(Category).where(Category.id == category_id))
        category = result.scalar_one_or_none()  
        if category is None:
            return None
        async with self.session:
            await self.session.delete(category)
            await self.session.commit()
            

def get_category_service(session: AsyncSession = Depends(get_session)) -> CategoryService:
    """
    Dependency to get a CategoryService instance with a session.

    :param session: An asynchronous database session.
    :return: A CategoryService instance.
    """
    return CategoryService(session)
