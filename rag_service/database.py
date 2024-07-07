from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:1234@localhost:5432/rag"

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
