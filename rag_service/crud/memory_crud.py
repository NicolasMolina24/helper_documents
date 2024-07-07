from typing import List
from sqlalchemy.orm import Session
from rag_service import models
from rag_service.schemas import memory_schema

# def get_memory(db: Session, user_id: int):
#     return db.query(memory.Memory).filter(memory.Memory.id == user_id).first()

def get_memories(db: Session, skip: int = 0, limit: int = 5) -> List[models.Memory]:
    """Get all memories from the database.
    
    Args:
        db (Session): SQLAlchemy session
        skip (int, optional): Number of memories to skip. Defaults to 0.
        limit (int, optional): Number of memories to limit. Defaults to 5.

    Returns:
        List[memory_model.Memory]: List of memories"""
    return (
        db.query(models.Memory)
        .order_by(models.Memory.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

def create_memory(db: Session, memory: memory_schema.MemoryCreate) -> models.Memory:
    """Create a new memory in the database.

    Args:
        db (Session): SQLAlchemy session
        memory (memory_schema.MemoryCreate): Memory data
        
    Returns:
        memory_model.Memory: Created memory"""
    db_memory = models.Memory(**memory.model_dump())
    db.add(db_memory)
    db.commit()
    db.refresh(db_memory)
    return db_memory
