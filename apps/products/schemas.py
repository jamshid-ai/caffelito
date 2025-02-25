from pydantic import BaseModel, Field
from typing import Optional

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = Field(None, description="The description of the product")

class ProductCreate(ProductBase):
    category_id: int

class ProductRead(ProductBase):
    id: int
    category_id: int

class ProductUpdate(ProductBase):
    category_id: Optional[int] = Field(None, description="The id of the category of the product")

class ProductPatch(ProductBase):
    category_id: Optional[int] = Field(None, description="The id of the category of the product")

