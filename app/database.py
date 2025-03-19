from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import DATABASE_URL

engine = create_engine(DATABASE_URL)

# Create a session factory to interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """
    Dependency function to get a database session.
    Ensures that the session is properly closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()