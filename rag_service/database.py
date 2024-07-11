from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
import os
import dotenv

dotenv.load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER_DB")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD_DB")
POSTGRES_DB = os.getenv("POSTGRES_DB_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST_DB")
POSTGRES_PORT = os.getenv("POSTGRES_PORT_DB")



SQLALCHEMY_DATABASE_URL = "postgresql://postgres:1234@localhost:5432/rag"
SQLALCHEMY_DATABASE_URL2 = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
print(SQLALCHEMY_DATABASE_URL2)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
)

# Create the database if it does not exist
if not database_exists(engine.url):
    create_database(engine.url)

# Create database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
