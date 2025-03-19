from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.auth import get_current_user
from app.database import get_db
from app.models import Post
from app.schemas import PostCreate, PostResponse
import redis

router = APIRouter()
cache = redis.Redis(host="localhost", port=6379, db=0)

@router.post("/addpost", response_model=PostResponse)
def add_post(post: PostCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    new_post = Post(text=post.text, owner_id=user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/getposts")
def get_posts(db: Session = Depends(get_db), user=Depends(get_current_user)):
    cache_key = f"posts:{user.id}"
    cached_posts = cache.get(cache_key)
    if cached_posts:
        return cached_posts
    
    posts = db.query(Post).filter(Post.owner_id == user.id).all()
    cache.setex(cache_key, 300, str(posts))  # Cache for 5 minutes
    return posts

@router.delete("/deletepost/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    post = db.query(Post).filter(Post.id == post_id, Post.owner_id == user.id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(post)
    db.commit()
    return {"message": "Post deleted successfully"}
