import pandas as pd
from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_db
from crud import memory_crud, document_crud
from rag import vectorstorage

def get_memory_dict(memory_object):
    """Get the memory object as a dictionary.
    
    Args:
        memory_object (Memory): Memory object"""
    memory_dict = dict(
        human_msg=memory_object.human_msg,
        ia_msg=memory_object.ia_msg,
        created_at=memory_object.created_at
    )
    return memory_dict

def get_context_memory(db: Session, limit: int = 5):
    """Get the context memory.
    
    Args:
        db (Session): SQLAlchemy session
        limit (int, optional): Number of memories to limit. Defaults to 5.
    
    Returns:
        """
    # split by comma and strip spaces
    result = memory_crud.get_memories(db, limit=limit)
    result = [get_memory_dict(memory) for memory in result]
    memory_df = pd.DataFrame(data=result)
    memory_df = memory_df.apply(
        lambda x: f"AIMessage(content={x['ia_msg']}), HumanMessage(content={x['human_msg']})", 
        axis=1)
    context_memory = "\n".join(memory_df)
    return context_memory

def get_context_docs(docs_ids: str, query: str, db: Session, limit: int = 10):
    """Get the context from the documents.
    
    Args:
        docs_ids (str): Comma separated string of document ids
        query (str): User query
        db (Session): SQLAlchemy session
        limit (int, optional): Number of documents to limit. Defaults to 10.
    
    Returns:
    """
    # split by comma and strip spaces
    docs_ids = [doc_id.strip() for doc_id in docs_ids.split(",")]
    print(docs_ids)
    docs = document_crud.get_documents(limit=limit, db=db)
    filtered_collections_name = [
        doc.collection_name for doc in docs if str(doc.id) in docs_ids]
    filtered_uris = [doc.uri for doc in docs if str(doc.id) in docs_ids]
    uri = filtered_uris[0]
    context_vs = vectorstorage.retriever_vectorstore(
        collections=filtered_collections_name, uri=uri, question=query)

    # call the rag
    return context_vs
