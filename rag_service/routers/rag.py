from sqlalchemy.orm import Session
from rag_service.crud import rag_crud
from fastapi import APIRouter, Depends
from rag_service.rag import generic_rag
from rag_service.database import get_db
from rag_service.rag import router as rag_router


router = APIRouter(prefix="/rag", tags=["Rag"])


@router.get("/rag_response")
def get_rag_route(
    docs_ids: str,
    question: str,
    db: Session = Depends(get_db)
):
    """Get the response from the RAG model"""
    memory_context = rag_crud.get_context_memory(db, limit=5)
    vector_storage_context = rag_crud.get_context_docs(
        docs_ids=docs_ids, query=question, db=db, limit=5)

    routed = rag_router.runnables_route_question(
        memory_context=memory_context,
        vector_storage_context=vector_storage_context,
        question=question)

    if routed.route == "Vector_storage":
        rag_out = generic_rag.runnable_conext(
            context=vector_storage_context, question=question)
    elif routed.route == "Memory":
        rag_out = generic_rag.runnable_conext(
            context=memory_context, question=question)
    else:
        rag_out = generic_rag.runnable_generic(question)
    return rag_out


@router.get("/rag_from_docs")
def get_context_memory(docs_ids: str, query: str, db: Session = Depends(get_db)):
    """Get the response from the RAG model based on the context from the vector storage"""
    # Get context from vector storage
    vector_storage_context = rag_crud.get_context_docs(
        docs_ids=docs_ids, query=query, db=db, limit=5)
    # Get RAG output
    rag_out = generic_rag.runnable_conext(
        context=vector_storage_context, question=query)
    return {rag_out: rag_out.content}
