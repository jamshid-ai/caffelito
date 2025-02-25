from pydantic import BaseModel

class CategoryBase(BaseModel):
    name: str
    description: str | None = None

class CategoryCreate(CategoryBase):
    pass

class CategoryRead(CategoryBase):
    id: int

class CategoryUpdate(CategoryBase):
    pass

class CategoryPatch(CategoryBase):
    pass
