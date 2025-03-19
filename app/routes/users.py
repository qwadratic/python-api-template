from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import UserCreate, Token
from app.logic.users import create_user, authenticate_user

router = APIRouter()

@router.post("/signup", response_model=Token)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    """
    Handles user signup and returns an authentication token.
    """
    token = create_user(user, db)
    return Token(access_token=token, token_type="bearer")

@router.post("/login", response_model=Token)
def login(user: UserCreate, db: Session = Depends(get_db)):
    """
    Handles user login and returns an authentication token.
    """
    token = authenticate_user(user.email, user.password, db)
    return Token(access_token=token, token_type="bearer")
