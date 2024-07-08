from typing import List
from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from rag_service.database import get_db
from rag_service.rag import router as rag_router
from rag_service.crud import document_crud


router = APIRouter(prefix="/rag", tags=["Rag"])


@router.get("/rag_route")
def get_rag_route(
    question: str
):
    """Get the last <limint> memories from the database """
    routed = rag_router.runnables_route_question(question=question)
    print(" HOLAAA ", routed)
    return routed.route


@router.get("/rag_docs")
def get_rag_docs(docs_ids: str, query: str, db: Session = Depends(get_db), limit: int = 10):
    # split by comma and strip spaces
    docs_ids = [doc_id.strip() for doc_id in docs_ids.split(",")]
    print(docs_ids)
    docs = document_crud.get_documents(limit=limit, db=db)
    filtered_collections_name = [doc.collection_name for doc in docs if str(doc.id) in docs_ids]
    filtered_uris = [doc.uri for doc in docs if str(doc.id) in docs_ids]

    # call the vector storage retriever and give it the filtered collections name 
    # collections = [doc.collection_name for doc in filtered_docs]

    return {'col': filtered_collections_name}


# @router.get("/rag_docs")
# def get_rag_docs(docs_ids: List[str], query: str):    
#     docs = document_crud.get_documents(docs_ids)
#     # get and select doc ids in docs_ids
#     filtered_docs = [doc_id for doc_id in docs_ids if doc_id.id in docs]
#     # load vectorstorage from uri 


    #generation = generate(List[docs], query) # [id], [URI][]
    # load vectorstorage
    # query vectorstorage
    # retriever ansuwer

    # pass #return memories

# @router.post("/{user_id}")
# def create_vectorstorage_endpoint():
#     #user = user_crud.get_user(user_id)
#     # if user:
#         # vs_id = vectorsatorage_crud.create_vectorstorage("query", "file_path", "URI")
#         # create_vectorstorage("query", "file_path", "URI")
#     # else: 
#         # Raise error
#     pass


# @router.post("/{user_id}")
# def update_vectorstorage_endpoint():
#     #user = user_crud.get_user(user_id)
#     # if user:

# @router.post("/", response_model=memory_schema.Memory, status_code=status.HTTP_201_CREATED)
# def create_memory(
#     memory: memory_schema.MemoryBase, db: Session = Depends(get_db)
# ):
#     """Create a new memory in the database"""
#     return memory_crud.create_memory(db, memory)


# # create vectorsorage / groups of files
# # add files to vectorstorage
# # load vectorsotrag" -> query relationship between files and uri for loading vectorstorage
# # get rag answer <- query human, + prompt + model_name + temperature
