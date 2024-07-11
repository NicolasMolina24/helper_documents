from typing import List
from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas import memory_schema
from crud import memory_crud

router = APIRouter(prefix="/memory", tags=["Memory"])


@router.get("/", response_model=List[memory_schema.Memory])
def get_memories(
    skip: int = 0, limit: int = 5, db: Session = Depends(get_db)
):
    """Get the last <limint> memories from the database """
    memories = memory_crud.get_memories(db, skip=skip, limit=limit)
    return memories

@router.post("/", response_model=memory_schema.Memory, status_code=status.HTTP_201_CREATED)
def create_memory(
    memory: memory_schema.MemoryBase, db: Session = Depends(get_db)
):
    """Create a new memory in the database"""
    return memory_crud.create_memory(db, memory)
