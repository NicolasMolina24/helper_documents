from fastapi import FastAPI
from rag_service.database import engine
from rag_service.routers  import memory, document
from rag_service import models

# create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Rag API",
    description="This is the API for the RAG service.",
    version="0.0.1",
)

app.include_router(memory.router)
app. include_router(document.router)