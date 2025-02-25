from fastapi import APIRouter, Depends
from apps.orders.services import get_order_service, OrderService
from apps.orders.schemas import OrderCreate, OrderRead, OrderUpdate, OrderPatch

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=OrderRead)
async def create_order(order: OrderCreate, service: OrderService = Depends(get_order_service)):
    return await service.create_order(order)

@router.get("/", response_model=list[OrderRead])
async def get_orders(page: int = 1, size: int = 10, service: OrderService = Depends(get_order_service)):
    return await service.get_orders(page, size)

@router.get("/{order_id}", response_model=OrderRead)
async def get_order_by_id(order_id: int, service: OrderService = Depends(get_order_service)):
    return await service.get_order_by_id(order_id)

@router.put("/{order_id}", response_model=OrderRead)
async def update_order(order_id: int, order: OrderUpdate, service: OrderService = Depends(get_order_service)):
    return await service.update_order(order_id, order)

@router.patch("/{order_id}", response_model=OrderRead)
async def patch_order(order_id: int, order: OrderPatch, service: OrderService = Depends(get_order_service)):
    return await service.patch_order(order_id, order)