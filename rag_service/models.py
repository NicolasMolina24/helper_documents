from datetime import datetime
from rag_service.database import Base
from sqlalchemy import Column, Integer, String, DateTime

class Memory(Base):
    __tablename__ = "memory"

    id = Column(Integer, primary_key=True)
    human_msg = Column(String, index=True)
    ia_msg = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.now)
    # updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

class Document(Base):
    __tablename__ = "document"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    name = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now) 

