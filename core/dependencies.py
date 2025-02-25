from fastapi import HTTPException, status, Depends
from core.jwt import JwtBearer, JWTHandler
from jose.exceptions import JWTError
from apps.users.services import UserService, get_user_service

class UserHandling:
    def __init__(self) -> None:
        pass

    async def user(self, token: str = Depends(JwtBearer()), service: UserService = Depends(get_user_service)):
        try:
            payload = await JWTHandler().decode_jwt(token)
            user = await UserHandling.determine_user(payload=payload, service=service)
            return user
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"}
            )

    @staticmethod
    async def determine_user(payload: dict, service: UserService):
        user_email = payload.get("sub")
        user = await service.get_user_by_email(user_email)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"}
            )
        return user

    async def token_data(self, token: str = Depends(JwtBearer())):
        try:
            payload = await JWTHandler().decode_jwt(token)
            return payload
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
