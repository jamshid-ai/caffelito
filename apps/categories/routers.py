from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List
from apps.categories.schemas import CategoryCreate, CategoryRead, CategoryUpdate, CategoryPatch
from apps.categories.services import CategoryService, get_category_service
from core.dependencies import UserHandling
from core.models import User

router = APIRouter()

@router.post("/categories", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
async def create_category(
        category: CategoryCreate,
        service: CategoryService = Depends(get_category_service),
        user: User = Depends(UserHandling().user)
):
    """
    Create a new category.

    :param category: The category data to create.
    :param service: The category service dependency.
    :param user: The authenticated user.
    :return: The created category.
    """
    return await service.create_category(category)

@router.get("/categories", response_model=List[CategoryRead])
async def read_categories(
        page: int = Query(1, ge=1),
        size: int = Query(10, ge=1, le=100),
        service: CategoryService = Depends(get_category_service),
        user: User = Depends(UserHandling().user)
):
    """
    Retrieve a list of categories with pagination.

    :param page: The page number to retrieve.
    :param size: The number of categories per page.
    :param service: The category service dependency.
    :param user: The authenticated user.
    :return: A list of categories.
    """
    categories = await service.get_categories(page, size)
    return categories

@router.get("/categories/{category_id}", response_model=CategoryRead)
async def read_category(
        category_id: int,
        service: CategoryService = Depends(get_category_service),
        user: User = Depends(UserHandling().user)
):
    """
    Retrieve a category by its ID.

    :param category_id: The ID of the category to retrieve.
    :param service: The category service dependency.
    :param user: The authenticated user.
    :return: The category if found, otherwise raises a 404 error.
    """
    category = await service.get_category_by_id(category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.put("/categories/{category_id}", response_model=CategoryRead)
async def update_category(
        category_id: int,
        data: CategoryUpdate,
        service: CategoryService = Depends(get_category_service),
        user: User = Depends(UserHandling().user)
):
    """
    Update a category by its ID.

    :param category_id: The ID of the category to update.
    :param data: The updated category data.
    :param service: The category service dependency.
    :param user: The authenticated user.
    :return: The updated category if found, otherwise raises a 404 error.
    """
    category = await service.update_category(category_id, data)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.patch("/categories/{category_id}", response_model=CategoryRead)
async def patch_category(
        category_id: int,
        data: CategoryPatch,
        service: CategoryService = Depends(get_category_service),
        user: User = Depends(UserHandling().user)
):
    """
    Partially update a category by its ID.

    :param category_id: The ID of the category to patch.
    :param data: The partial category data to update.
    :param service: The category service dependency.
    :param user: The authenticated user.
    :return: The updated category if found, otherwise raises a 404 error.
    """
    category = await service.patch_category(category_id, data)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
        category_id: int,
        service: CategoryService = Depends(get_category_service),
        user: User = Depends(UserHandling().user)
):
    """
    Delete a category by its ID.

    :param category_id: The ID of the category to delete.
    :param service: The category service dependency.
    :param user: The authenticated user.
    :return: A success message if the category is deleted.
    """
    await service.delete_category(category_id)
    return {"message": "Category deleted successfully"}
