from fastapi import HTTPException, status, Depends
from core.jwt import JwtBearer, JWTHandler
from jose.exceptions import JWTError
from apps.users.services import UserService, get_user_service

class UserHandling:
    def __init__(self) -> None:
        # Initialize the UserHandling class
        pass

    async def user(self, token: str = Depends(JwtBearer()), service: UserService = Depends(get_user_service)):
        # Method to retrieve a user based on a JWT token
        try:
            # Decode the JWT token to get the payload
            payload = await JWTHandler().decode_jwt(token)
            # Determine the user from the payload and service
            user = await UserHandling.determine_user(payload=payload, service=service)
            return user
        except JWTError:
            # Raise an HTTP exception if the token is invalid
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"}
            )

    @staticmethod
    async def determine_user(payload: dict, service: UserService):
        # Static method to determine the user from the payload
        user_email = payload.get("sub")  # Extract the user email from the payload
        user = await service.get_user_by_email(user_email)  # Retrieve the user by email
        if user is None:
            # Raise an HTTP exception if the user is not found
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"}
            )
        return user

    async def token_data(self, token: str = Depends(JwtBearer())):
        # Method to retrieve the payload data from a JWT token
        try:
            # Decode the JWT token to get the payload
            payload = await JWTHandler().decode_jwt(token)
            return payload
        except JWTError:
            # Raise an HTTP exception if the token is invalid
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
