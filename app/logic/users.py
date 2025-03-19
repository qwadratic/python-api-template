from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.auth import get_password_hash, verify_password, create_access_token
from app.models import User
from app.schemas import UserCreate

def create_user(user: UserCreate, db: Session) -> str:
    """
    Registers a new user and returns an authentication token.
    
    Args:
        user (UserCreate): User signup data.
        db (Session): Database session.
    
    Returns:
        str: JWT authentication token.
    
    Raises:
        HTTPException: If email is already registered.
    """
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")

    hashed_password = get_password_hash(user.password)
    new_user = User(email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return create_access_token({"sub": new_user.id})

def authenticate_user(email: str, password: str, db: Session) -> str:
    """
    Authenticates a user and returns a JWT token.
    
    Args:
        email (str): User email.
        password (str): User password.
        db (Session): Database session.
    
    Returns:
        str: JWT token if authentication succeeds.
    
    Raises:
        HTTPException: If credentials are invalid.
    """
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    return create_access_token({"sub": user.id})