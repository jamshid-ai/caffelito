from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from core.connections import get_session
from core.models import Order, OrderProduct
from apps.orders.schemas import OrderCreate, OrderRead, OrderUpdate, OrderPatch

class OrderService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_order(self, order: OrderCreate) -> OrderRead:
        async with self.session:
            new_order = Order(**order.model_dump())
            self.session.add(new_order)
            await self.session.commit()
            await self.session.refresh(new_order)
        return OrderRead.model_validate(new_order)
    
    async def get_orders(self, page: int, size: int) -> list[OrderRead]:
        async with self.session:
            query = select(Order).offset((page - 1) * size).limit(size)
            result = await self.session.execute(query)
            orders = result.scalars().all()
            return [OrderRead.model_validate(order) for order in orders]
        
    async def get_order_by_id(self, order_id: int) -> OrderRead | None:
        async with self.session:
            query = select(Order).where(Order.id == order_id)
            result = await self.session.execute(query)
            order = result.scalar_one_or_none()
            return OrderRead.model_validate(order) if order else None

    async def update_order(self, order_id: int, order: OrderUpdate) -> OrderRead | None:
        async with self.session:
            result = await self.session.execute(select(Order).where(Order.id == order_id))
            order = result.scalar_one_or_none()
            if order:
                order.user_id = order.user_id
                await self.session.commit()
                await self.session.refresh(order)
                return OrderRead.model_validate(order)
            return None
        
    async def patch_order(self, order_id: int, order: OrderPatch) -> OrderRead | None:
        async with self.session:
            result = await self.session.execute(select(Order).where(Order.id == order_id))
            order = result.scalar_one_or_none()
            if order:
                order.user_id = order.user_id
                await self.session.commit()
                await self.session.refresh(order)
                return OrderRead.model_validate(order)
            return None
        
    async def delete_order(self, order_id: int) -> None:
        async with self.session:
            result = await self.session.execute(select(Order).where(Order.id == order_id))
            order = result.scalar_one_or_none()
            if order:
                await self.session.delete(order)
                await self.session.commit()

def get_order_service(session: AsyncSession = Depends(get_session)):
    return OrderService(session)