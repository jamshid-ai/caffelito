from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from core.connections import get_session
from core.models import Product
from apps.products.schemas import ProductCreate, ProductRead, ProductUpdate, ProductPatch


class ProductService:
    """
    Service class to handle operations related to products.
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize the ProductService with a database session.

        :param session: An asynchronous database session.
        """
        self.session = session

    async def create_product(self, product: ProductCreate) -> ProductRead:
        """
        Create a new product.

        :param product: The product data to create.
        :return: The created product.
        """
        async with self.session:
            new_product = Product(**product.model_dump())
            self.session.add(new_product)
            await self.session.commit()
            await self.session.refresh(new_product)
        return ProductRead.model_validate(new_product)
    
    async def get_products(self, page: int, size: int) -> list[ProductRead]:
        """
        Retrieve a list of products with pagination.

        :param page: The page number to retrieve.
        :param size: The number of products per page.
        :return: A list of products.
        """
        async with self.session:
            query = select(Product).offset((page - 1) * size).limit(size)
            result = await self.session.execute(query)
            products = result.scalars().all()
            return [ProductRead.model_validate(product) for product in products]
        
    async def get_product_by_id(self, product_id: int) -> ProductRead | None:
        """
        Retrieve a product by its ID.

        :param product_id: The ID of the product to retrieve.
        :return: The product if found, otherwise None.
        """
        async with self.session:
            query = select(Product).where(Product.id == product_id)
            result = await self.session.execute(query)
            product = result.scalar_one_or_none()
            return ProductRead.model_validate(product) if product else None
        
    async def update_product(self, product_id: int, product: ProductUpdate) -> ProductRead | None:
        """
        Update a product by its ID.

        :param product_id: The ID of the product to update.
        :param product: The updated product data.
        :return: The updated product if found, otherwise None.
        """
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
        """
        Partially update a product by its ID.

        :param product_id: The ID of the product to patch.
        :param product: The partial product data to update.
        :return: The updated product if found, otherwise None.
        """
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
        """
        Delete a product by its ID.

        :param product_id: The ID of the product to delete.
        """
        async with self.session:
            result = await self.session.execute(select(Product).where(Product.id == product_id))
            product = result.scalar_one_or_none()
            if product:
                await self.session.delete(product)
                await self.session.commit()

def get_product_service(session: AsyncSession = Depends(get_session)):
    """
    Dependency to get a ProductService instance with a session.

    :param session: An asynchronous database session.
    :return: A ProductService instance.
    """
    return ProductService(session)
