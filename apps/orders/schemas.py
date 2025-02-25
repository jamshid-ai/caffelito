from pydantic import BaseModel

from apps.products.schemas import ProductRead

class OrderCreate(BaseModel):
    user_id: int
    product_ids: list[int]

class OrderRead(BaseModel):
    id: int
    user_id: int
    products: list[ProductRead]

class OrderUpdate(BaseModel):
    user_id: int
    product_ids: list[int]

class OrderPatch(BaseModel):
    user_id: int
    product_ids: list[int]

class OrderProductCreate(BaseModel):
    order_id: int
    product_id: int

class OrderProductRead(BaseModel):
    id: int
    order_id: int
    product_id: int

class OrderProductPatch(BaseModel):
    product_id: int
    quantity: int

class OrderProductUpdate(BaseModel):
    product_id: int
    quantity: int

class OrderProductDelete(BaseModel):
    product_id: int
