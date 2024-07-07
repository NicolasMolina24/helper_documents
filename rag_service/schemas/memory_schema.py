from pydantic import BaseModel
from datetime import datetime

class MemoryBase(BaseModel):
    human_msg: str
    ia_msg: str

# class for writing data
class MemoryCreate(MemoryBase):
    created_at: datetime

# class for reading
class Memory(MemoryCreate):
    id: int

    class Config:
        from_attributes = True
