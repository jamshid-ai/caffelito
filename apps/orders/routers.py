from fastapi import APIRouter, Depends
from apps.orders.services import get_order_service, OrderService
from apps.orders.schemas import OrderCreate, OrderRead, OrderUpdate, OrderPatch

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=OrderRead)
async def create_order(order: OrderCreate, service: OrderService = Depends(get_order_service)):
    """
    Create a new order.

    :param order: The order data to create.
    :param service: The order service dependency.
    :return: The created order.
    """
    return await service.create_order(order)

@router.get("/", response_model=list[OrderRead])
async def get_orders(page: int = 1, size: int = 10, service: OrderService = Depends(get_order_service)):
    """
    Retrieve a list of orders with pagination.

    :param page: The page number to retrieve.
    :param size: The number of orders per page.
    :param service: The order service dependency.
    :return: A list of orders.
    """
    return await service.get_orders(page, size)

@router.get("/{order_id}", response_model=OrderRead)
async def get_order_by_id(order_id: int, service: OrderService = Depends(get_order_service)):
    """
    Retrieve an order by its ID.

    :param order_id: The ID of the order to retrieve.
    :param service: The order service dependency.
    :return: The order if found, otherwise raises a 404 error.
    """
    return await service.get_order_by_id(order_id)

@router.put("/{order_id}", response_model=OrderRead)
async def update_order(order_id: int, order: OrderUpdate, service: OrderService = Depends(get_order_service)):
    """
    Update an order by its ID.

    :param order_id: The ID of the order to update.
    :param order: The updated order data.
    :param service: The order service dependency.
    :return: The updated order if found, otherwise raises a 404 error.
    """
    return await service.update_order(order_id, order)

@router.patch("/{order_id}", response_model=OrderRead)
async def patch_order(order_id: int, order: OrderPatch, service: OrderService = Depends(get_order_service)):
    """
    Partially update an order by its ID.

    :param order_id: The ID of the order to patch.
    :param order: The partial order data to update.
    :param service: The order service dependency.
    :return: The updated order if found, otherwise raises a 404 error.
    """
    return await service.patch_order(order_id, order)