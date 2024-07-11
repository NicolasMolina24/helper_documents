from sqlalchemy.orm import Session
import models
from schemas import document_schema
from typing import List


def get_document_by_name(db: Session, name: str) -> models.Document:
    """Get a document by name from the database.

    Args:
        db (Session): SQLAlchemy session
        name (str): Document name

    Returns:
        models.Document: Document"""
    return db.query(models.Document).filter(models.Document.name == name).first()

def get_documents(
    db: Session, skip: int = 0, limit: int = 5
) -> List[models.Document]:
    """Get all documents from the database.

    Args:
        db (Session): SQLAlchemy session
        skip (int, optional): Number of documents to skip. Defaults to 0.
        limit (int, optional): Number of documents to limit. Defaults to 5.

    Returns:
        List[models.Document]: List of documents"""
    return (
        db.query(models.Document)
        .order_by(models.Document.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

def create_document(
    db: Session, document: document_schema.DocumentCreate
) -> models.Document:
    """Create a new document in the database.

    Args:
        db (Session): SQLAlchemy session
        document (documents_schema.DocumentCreate): Document data

    Returns:
        models.Document: Created document"""
    db_document = models.Document(**document.model_dump())
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document
