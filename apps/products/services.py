from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from core.connections import get_session
from core.models import Product
from apps.products.schemas import ProductCreate, ProductRead, ProductUpdate, ProductPatch


class ProductService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_product(self, product: ProductCreate) -> ProductRead:
        async with self.session:
            new_product = Product(**product.model_dump())
            self.session.add(new_product)
            await self.session.commit()
            await self.session.refresh(new_product)
        return ProductRead.model_validate(new_product)
    
    async def get_products(self, page: int, size: int) -> list[ProductRead]:
        async with self.session:
            query = select(Product).offset((page - 1) * size).limit(size)
            result = await self.session.execute(query)
            products = result.scalars().all()
            return [ProductRead.model_validate(product) for product in products]
        
    async def get_product_by_id(self, product_id: int) -> ProductRead | None:
        async with self.session:
            query = select(Product).where(Product.id == product_id)
            result = await self.session.execute(query)
            product = result.scalar_one_or_none()
            return ProductRead.model_validate(product) if product else None
        
    async def update_product(self, product_id: int, product: ProductUpdate) -> ProductRead | None:
        async with self.session:
            result = await self.session.execute(select(Product).where(Product.id == product_id))
            product = result.scalar_one_or_none()
            if product:
                product.name = product.name
                product.description = product.description
                product.category_id = product.category_id
                await self.session.commit()
                await self.session.refresh(product)
                return ProductRead.model_validate(product)
            return None
        
    async def patch_product(self, product_id: int, product: ProductPatch) -> ProductRead | None:
        async with self.session:
            result = await self.session.execute(select(Product).where(Product.id == product_id))
            product = result.scalar_one_or_none()
            if product:
                product.name = product.name
                product.description = product.description
                product.category_id = product.category_id
                await self.session.commit()
                await self.session.refresh(product)
                return ProductRead.model_validate(product)
            return None
        
    async def delete_product(self, product_id: int) -> None:
        async with self.session:
            result = await self.session.execute(select(Product).where(Product.id == product_id))
            product = result.scalar_one_or_none()
            if product:
                await self.session.delete(product)
                await self.session.commit()

def get_product_service(session: AsyncSession = Depends(get_session)):
    return ProductService(session)
