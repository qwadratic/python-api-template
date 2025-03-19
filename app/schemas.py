from pydantic import BaseModel, EmailStr, Field
from typing import Annotated

class UserCreate(BaseModel):
    email: EmailStr
    password: Annotated[str, Field(min_length=6)]

class UserResponse(BaseModel):
    id: int
    email: EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str

class PostCreate(BaseModel):
    text: Annotated[str, Field(max_length=1024 * 1024)]  # Limit to 1MB

class PostResponse(BaseModel):
    id: int
    text: str
    owner_id: int
