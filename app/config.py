import os
from dotenv import load_dotenv

load_dotenv()

# Replace with MySQL URL
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+mysqlconnector://user:password@localhost/db_name")

# Security configurations for JWT authentication
SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
ALGORITHM = "HS256"
TOKEN_EXPIRATION = 3600  # 1 hour in seconds

