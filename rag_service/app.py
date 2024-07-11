from fastapi import FastAPI
from database import engine
from routers  import memory, document, rag
import models
import dotenv

dotenv.load_dotenv()
# create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Rag API",
    description="This is the API for the RAG service.",
    version="0.0.1",
)

app.include_router(memory.router)
app.include_router(document.router)
app.include_router(rag.router)
