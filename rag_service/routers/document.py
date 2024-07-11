from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas import document_schema
from crud import document_crud

router = APIRouter(prefix="/document", tags=["Document"])


@router.get("/", response_model=List[document_schema.Document])
def read_documents(skip: int = 0, limit: int = 5, db: Session = Depends(get_db)):
    """Get the last <limint> documents from the database"""
    documents = document_crud.get_documents(db, skip=skip, limit=limit)
    return documents


@router.post("/", response_model=document_schema.Document)
def create_document(
    document: document_schema.DocumentBase, db: Session = Depends(get_db)
):
    """Create a new document in the database"""
    doc_name = document_crud.get_document_by_name(db=db, name=document.name)
    if doc_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Document name already exists",
        )
    return document_crud.create_document(db=db, document=document)
