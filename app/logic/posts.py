from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models import Post, User
from app.schemas import PostCreate
import redis

# Initialize Redis for caching
cache = redis.Redis(host="localhost", port=6379, db=0)

def create_post(post: PostCreate, user: User, db: Session) -> Post:
    """
    Creates a new post for a user.
    
    Args:
        post (PostCreate): Post data.
        user (User): Authenticated user.
        db (Session): Database session.
    
    Returns:
        Post: The newly created post.
    """
    new_post = Post(text=post.text, owner_id=user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

def get_user_posts(user: User, db: Session):
    """
    Retrieves all posts for a user, with caching.
    
    Args:
        user (User): Authenticated user.
        db (Session): Database session.
    
    Returns:
        List[Post]: List of posts.
    """
    cache_key = f"posts:{user.id}"
    cached_posts = cache.get(cache_key)
    if cached_posts:
        return cached_posts  # Retrieve from cache if available

    posts = db.query(Post).filter(Post.owner_id == user.id).all()
    cache.setex(cache_key, 300, str(posts))  # Cache for 5 minutes
    return posts

def delete_post(post_id: int, user: User, db: Session):
    """
    Deletes a user's post.
    
    Args:
        post_id (int): ID of the post.
        user (User): Authenticated user.
        db (Session): Database session.
    
    Returns:
        dict: Confirmation message.
    
    Raises:
        HTTPException: If post not found or user is unauthorized.
    """
    post = db.query(Post).filter(Post.id == post_id, Post.owner_id == user.id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    db.delete(post)
    db.commit()
    return {"message": "Post deleted successfully"}