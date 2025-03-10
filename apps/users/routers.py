from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.params import Query
from sqlalchemy.orm import Session
from typing import List

from apps.users.services import get_user_service, UserService
from apps.users.schemas import UserCreate, UserLogin, UserPatch, UserRead, UserUpdate
from core.dependencies import UserHandling
from core.jwt import JWTHandler
from core.models import User
from core.security import verify_password

router = APIRouter()

@router.post("/registration", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, service: UserService = Depends(get_user_service)):
    """
    Register a new user.

    :param user: The user data to create.
    :param service: The user service dependency.
    :return: The created user.
    """
    db_user = await service.get_user_by_email(user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await service.create_user(user)

@router.post("/authentication")
async def authenticate_user(user: UserLogin, service: UserService = Depends(get_user_service)):
    """
    Authenticate a user and return a JWT token.

    :param user: The login credentials.
    :param service: The user service dependency.
    :return: A dictionary containing the access token and token type.
    """
    db_user = await service.get_user_by_username(user.username)
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = await JWTHandler().create_token(db_user)
    return {"access_token": token, "token_type": "Bearer"}

@router.post("/verification")
async def verification(
        user: User = Depends(UserHandling().user),
        service: UserService = Depends(get_user_service)
):
    """
    Verify a user's account.

    :param user: The authenticated user.
    :param service: The user service dependency.
    :return: The verified user.
    """
    if user.is_verified:
        raise HTTPException(status_code=400, detail="User already verified")
    # TODO: send verification email
    # token = await service.create_verification_token(user)
    return user

# @router.get("/verification/{token}")
# async def verify_user(token: str, service: UserService = Depends(get_user_service)):
#     user = await service.verify_user_by_token(token)
#     if not user:
#         raise HTTPException(status_code=400, detail="Invalid or expired token")

@router.get("/me", response_model=UserRead)
async def get_me(user: User = Depends(UserHandling().user)):
    """
    Retrieve the authenticated user's information.

    :param user: The authenticated user.
    :return: The user's information.
    """
    return user

@router.get("/users", response_model=List[UserRead])
async def read_users(
        page: int = Query(1, ge=1),
        size: int = Query(10, ge=1, le=100),
        service: UserService = Depends(get_user_service),
        user: User = Depends(UserHandling().user)
):
    """
    Retrieve a list of users with pagination.

    :param page: The page number to retrieve.
    :param size: The number of users per page.
    :param service: The user service dependency.
    :param user: The authenticated user.
    :return: A list of users.
    """
    users = await service.get_users(page, size)
    return users

@router.get("/users/{user_id}", response_model=UserRead)
async def read_user(
        user_id: int,
        service: UserService = Depends(get_user_service),
        user: User = Depends(UserHandling().user)
):
    """
    Retrieve a user by their ID.

    :param user_id: The ID of the user to retrieve.
    :param service: The user service dependency.
    :param user: The authenticated user.
    :return: The user if found, otherwise raises a 404 error.
    """
    db_user = await service.get_user_by_id(user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/users/{user_id}", response_model=UserRead)
async def update_user(
        user_id: int,
        data: UserUpdate,
        service: UserService = Depends(get_user_service),
        user: User = Depends(UserHandling().user)
):
    """
    Update a user by their ID.

    :param user_id: The ID of the user to update.
    :param data: The updated user data.
    :param service: The user service dependency.
    :param user: The authenticated user.
    :return: The updated user if found, otherwise raises a 404 error.
    """
    db_user = await service.update_user(user_id, data)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.patch("/users/{user_id}", response_model=UserRead)
async def patch_user(
        user_id: int,
        data: UserPatch,
        service: UserService = Depends(get_user_service),
        user: User = Depends(UserHandling().user)
):
    """
    Partially update a user by their ID.

    :param user_id: The ID of the user to patch.
    :param data: The partial user data to update.
    :param service: The user service dependency.
    :param user: The authenticated user.
    :return: The updated user if found, otherwise raises a 404 error.
    """
    db_user = await service.patch_user(user_id, data)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
        user_id: int,
        service: UserService = Depends(get_user_service),
        user: User = Depends(UserHandling().user)
):
    """
    Delete a user by their ID.

    :param user_id: The ID of the user to delete.
    :param service: The user service dependency.
    :param user: The authenticated user.
    :return: A success message if the user is deleted.
    """
    await service.delete_user(user_id)
    return {"message": "User deleted successfully"}
