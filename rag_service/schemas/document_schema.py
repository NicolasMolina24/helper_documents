from pydantic import BaseModel
from datetime import datetime

# base class
class DocumentBase(BaseModel):
    name: str

# write data
class DocumentCreate(DocumentBase):
    created_at: datetime

class DocumentUpdate(DocumentCreate):
    updated_at: datetime

# read data
class Document(DocumentUpdate):
    id: int

    class Config:
        from_attributes = True
