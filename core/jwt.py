from datetime import datetime, timedelta
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import HTTPException, Request, status
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTError
from time import time
from core.models import User
from core.config import settings


class JWTHandler:
    def __init__(self) -> None:
        pass

    async def decode_jwt(self, token: str):
        try:
            decode_token = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM],
                audience="users",
                issuer="auth"
                )
            return decode_token if decode_token['exp'] >= time() else None
        except ExpiredSignatureError or JWTError:
            return {}

    async def create_token(self, user: User):
        issuer = "auth"
        audience = "users"
        expires_delta = timedelta(days=1)
        expire = datetime.utcnow() + expires_delta
        to_encode = {"sub": user.email, "exp": expire, "iss": issuer, "aud": audience}
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt


class JwtBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JwtBearer, self).__init__(auto_error=True)

    async def __call__(self, request: Request):

        credentials: HTTPAuthorizationCredentials = await super(
            JwtBearer, self).__call__(request)

        if credentials:
            if not credentials.scheme == 'Bearer':
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Invalid or Expaired Token!"
                )
            token_status = await self.verify_jwt(
                jwtoken=credentials.credentials)
            if not token_status:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Invalid or Expaired Token!"
                )
            return credentials.credentials
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid or Expaired Token!"
            )

    async def verify_jwt(self, jwtoken: str):
        is_token_valid: bool = False  # a false flag
        payload = await JWTHandler().decode_jwt(token=jwtoken)
        if payload:
            is_token_valid = True
        return is_token_valid
