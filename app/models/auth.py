from pydantic import BaseModel, EmailStr
from typing import Optional
from app.orm import UserRole

# --- Token Schemas ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# --- User Schemas ---
class UserBase(BaseModel):
    name: str
    email: EmailStr
    phone: str
    role: UserRole

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True


from typing import Optional, List

from pydantic import BaseModel


class AuthRequest(BaseModel):
    username: str
    password: str