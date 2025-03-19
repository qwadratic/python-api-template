from pydantic import BaseModel, EmailStr, Field
from typing import Annotated, List

class UserCreate(BaseModel):
    """
    Schema for user signup and login request.

    Attributes:
        email (str): User email (validated as an email address).
        password (str): Password with a minimum length of 6 characters.
    """
    email: EmailStr
    password: Annotated[str, Field(min_length=6)]

class UserResponse(BaseModel):
    """
    Response schema for user details.

    Attributes:
        id (int): User ID.
        email (str): User email.
    """
    id: int
    email: EmailStr

class Token(BaseModel):
    """
    Schema for authentication token response.

    Attributes:
        access_token (str): JWT access token.
        token_type (str): Type of token (e.g., "bearer").
    """
    access_token: str
    token_type: str

class PostCreate(BaseModel):
    """
    Schema for creating a new post.

    Attributes:
        text (str): Content of the post (max size: 1MB).
    """
    text: Annotated[str, Field(max_length=1024 * 1024)]  # Limit to 1MB

class PostResponse(BaseModel):
    """
    Response schema for post details.

    Attributes:
        id (int): Post ID.
        text (str): Content of the post.
        owner_id (int): ID of the user who created the post.
    """
    id: int
    text: str
    owner_id: int

class PostListResponse(BaseModel):
    """
    Response schema for listing all posts of a user.
    
    Attributes:
        posts (List[PostResponse]): List of posts belonging to the user.
    """
    posts: List[PostResponse]
