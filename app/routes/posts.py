from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.auth import get_current_user
from app.database import get_db
from app.models import User
from app.schemas import PostCreate, PostListResponse, PostResponse
from app.logic.posts import create_post, get_user_posts, delete_post

router = APIRouter()

@router.post("/addpost", response_model=PostResponse)
def add_post(post: PostCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    """
    Handles adding a new post.
    """
    new_post = create_post(post, user, db)
    return PostResponse(
        id=new_post.id, 
        text=new_post.text, 
        owner_id=new_post.owner_id)

@router.get("/getposts")
def get_posts(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    """
    Retrieves all posts for the authenticated user.
    """
    user_posts = get_user_posts(user, db)
    return PostListResponse(posts=[
        PostResponse(id=p.id, text=p.text, owner_id=p.owner_id)
        for p in user_posts
    ])

@router.delete("/deletepost/{post_id}")
def remove_post(post_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    """
    Deletes a specific post owned by the authenticated user.
    """
    return delete_post(post_id, user, db)