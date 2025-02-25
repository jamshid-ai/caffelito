from fastapi import APIRouter, Depends, Query, status
from apps.products.services import get_product_service, ProductService
from apps.products.schemas import ProductCreate, ProductRead, ProductUpdate, ProductPatch
from core.dependencies import UserHandling
from core.models import User

router = APIRouter()

@router.post("/", response_model=ProductRead)
async def create_product(
        product: ProductCreate,
        service: ProductService = Depends(get_product_service),
        user: User = Depends(UserHandling().user)
):
    return await service.create_product(product)

@router.get("/", response_model=list[ProductRead])
async def get_products(
        page: int = Query(default=1, ge=1),
        size: int = Query(default=10, ge=1, le=100),
        service: ProductService = Depends(get_product_service),
        user: User = Depends(UserHandling().user),
):
    return await service.get_products(page, size)

@router.get("/{product_id}", response_model=ProductRead)
async def get_product_by_id(
        product_id: int,
        service: ProductService = Depends(get_product_service),
        user: User = Depends(UserHandling().user),
):
    return await service.get_product_by_id(product_id)

@router.put("/{product_id}", response_model=ProductRead)
async def update_product(
        product_id: int,
        product: ProductUpdate,
        service: ProductService = Depends(get_product_service),
        user: User = Depends(UserHandling().user),
):
    return await service.update_product(product_id, product)

@router.patch("/{product_id}", response_model=ProductRead)
async def patch_product(
        product_id: int,
        product: ProductPatch,
        service: ProductService = Depends(get_product_service),
        user: User = Depends(UserHandling().user),
):
    return await service.patch_product(product_id, product)

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
        product_id: int,
        service: ProductService = Depends(get_product_service),
        user: User = Depends(UserHandling().user),
):
    await service.delete_product(product_id)