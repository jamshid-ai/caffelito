from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserRead(BaseModel):
    id: int
    email: str
    username: str
    is_active: bool
    is_verified: bool
    role: str
    
class UserUpdate(BaseModel):
    email: str | None = None
    username: str | None = None
    is_active: bool | None = None
    is_verified: bool | None = None
    role: str | None = None

class UserPatch(BaseModel):
    email: str | None = None
    username: str | None = None
