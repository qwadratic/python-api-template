from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    """
    Database model for a user.
    
    Attributes:
        id (int): Primary key identifier for the user.
        email (str): Unique email address of the user.
        hashed_password (str): Hashed password for authentication.
        posts (relationship): Relationship to the Post model.
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    posts = relationship("Post", back_populates="owner")

class Post(Base):
    """
    Database model for a post.

    Attributes:
        id (int): Primary key identifier for the post.
        text (str): Content of the post.
        owner_id (int): Foreign key reference to the User model.
        owner (relationship): Relationship to the User model.
    """
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="posts")