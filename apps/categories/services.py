
from fastapi import Depends
from sqlalchemy import select
from apps.categories.schemas import CategoryCreate, CategoryRead, CategoryUpdate, CategoryPatch
from core.connections import get_session
from core.models import Category
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List


class CategoryService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_category(self, category: CategoryCreate) -> CategoryRead:
        async with self.session:
            self.session.add(category)
            await self.session.commit()
            await self.session.refresh(category)
        return category

    async def get_categories(self, page: int, size: int) -> List[CategoryRead]:
        async with self.session:
            result = await self.session.execute(select(Category).offset((page - 1) * size).limit(size))
        return result.scalars().all()

    async def get_category_by_id(self, category_id: int) -> CategoryRead | None:
        async with self.session:
            result = await self.session.execute(select(Category).where(Category.id == category_id))
        return result.scalar_one_or_none()

    async def update_category(self, category_id: int, data: CategoryUpdate) -> CategoryRead | None:
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
        async with self.session:
            result = await self.session.execute(select(Category).where(Category.id == category_id))
        category = result.scalar_one_or_none()  
        if category is None:
            return None
        async with self.session:
            await self.session.delete(category)
            await self.session.commit()
            

def get_category_service(session: AsyncSession = Depends(get_session)) -> CategoryService:
    return CategoryService(session)
