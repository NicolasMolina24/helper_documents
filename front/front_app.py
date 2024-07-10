import requests
import pandas as pd
import streamlit as st
from pathlib import Path
from pypdf import PdfReader
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_milvus.vectorstores import Milvus
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import os

load_dotenv()


def register_memory(human_msg, ia_msg, uri_service):
    """Register the conversation in the database
    
    Args:
        human_msg (str): Human message
        ia_msg (str): IA message
        uri_service (str): URI of the service
    
    Returns:
        dict: Response of the service"""
    # load the endpoint from the service
    uri_service += "memory/"
    # create the data to send
    data = {"human_msg": human_msg, "ia_msg": ia_msg}
    # send the data to the service
    response_post = requests.post(
        uri_service, json=data, timeout=10
    )  # Timeout after 10 seconds
    return response_post.json()


def register_document(name, uri_vs, file_type, collection_name, uri_service):
    """Register the document in the database
    
    Args:
        name (str): Name of the document
        uri_vs (str): URI of the vector store
        file_type (str): Type of the file
        collection_name (str): Name of the collection
        uri_service (str): URI of the service
    
    Returns:
        dict: Response of the service"""
    # load the endpoint from the service
    uri_service += "document/"
    # create the data to send
    data = {
        "name": name,
        "uri": uri_vs,
        "type": file_type,
        "collection_name": collection_name,
    }
    # send the data to the service
    response_post = requests.post(
        uri_service, json=data, timeout=10
    )  # Timeout after 10 seconds
    json_response = response_post.json()

    # add the id of new doc to the list
    st.session_state.documents_to_search_in.append(json_response["id"])
    return json_response


def get_documents(uri_service):
    """Get the documents in the database
    
    Args:
        uri_service (str): URI of the service
    
    Returns:
        dict: Response of the service"""
    # load the endpoint from the service
    uri_service += "document/"
    # create the data to send
    data = {
        "skip": 0,
        "limit": 10,
    }
    # send the data to the service
    # Timeout after 10 seconds
    response_get = requests.get(uri_service, json=data, timeout=10)
    return response_get.json()


def pdf_to_docs(doc):
    """Convert a PDF to a list of documents
    
    Args:
        doc (file): PDF file
    
    Returns:
        list: List of documents"""
    list_docs = []
    pdf = PdfReader(doc)
    for n, page in enumerate(pdf.pages):
        list_docs.append(
            Document(
                page_content=page.extract_text(),
                metadata={"source": doc.name, "type": doc.type, "page": str(n)},
            )
        )

    text_splitter = RecursiveCharacterTextSplitter(
        # Set a really small chunk size, just to show.
        chunk_size=1024,
        chunk_overlap=32,
        length_function=len,
        is_separator_regex=False,
    )
    chunks = text_splitter.split_documents(list_docs)
    return chunks


def create_collection(uri, collection_name, docs, embeddings):
    """Create a collection in Milvus
    
    Args:
        uri (str): URI of the Milvus
        collection_name (str): Name of the collection
        docs (list): List of documents
        embeddings (Embeddings): Embeddings object
    """
    print("Creating collection", collection_name)
    Milvus.from_documents(
        documents=docs,
        embedding=embeddings,
        connection_args={
            "uri": uri,
        },
        collection_name=collection_name,
        drop_old=True,  # Drop the old Milvus collection if it exists
    )
    


def load_docs(docs, uri_vs, uri_service, documents_in_bd):
    """Load the documents in the database
    
    Args:
        docs (list): List of documents
        uri_vs (str): URI of the Milvus
        uri_service (str): URI of the service
        documents_in_bd (list): List of documents in the database
    """
    for doc in docs:
        # doc name
        doc_name = Path(doc.name)
        # collections_name
        collection_name = doc_name.stem.lower().replace(" ", "_")
        doc_name = str(doc_name)
        # check if the document is already in the database
        if doc_name in documents_in_bd:
            st.warning(f"{doc.name} already exists in the database")
            continue
        # Get chunks for the document
        chunks_pdf = pdf_to_docs(doc)
        # create a collection for the document
        create_collection(uri_vs, doc_name, chunks_pdf, OpenAIEmbeddings())
        # register the document in the service
        register_document(doc_name, uri_vs, doc.type, collection_name, uri_service)
        st.success(f"Document {doc.name} loaded successfully", icon="✅")


# Streamed response emulator
def response_generator(uri_service, question):
    """Generate a response from the service
    
    Args:
        uri_service (str): URI of the service
        question (str): Question to ask
    
    Returns:
        dict: Response of the service"""
    # load the endpoint from the service
    uri_service += "rag_response/"
    # create the data to send
    data = {"docs_ids": st.session_state.documents_to_search_in, "question": question}
    # send the data to the service
    response_post = requests.post(
        uri_service, json=data, timeout=10
    )  # Timeout after 10 seconds
    return response_post.json()



def main(uri_service, uri_milvus):
    """Main function of the app

    Args:
        uri_service (str): URI of the service
        uri_milvus (str): URI of the Milvus
    """
    st.set_page_config(
        page_title="Chat with your docs", page_icon=":green_book:", layout="wide"
    )
    st.title("DocChat App")
    st.header("Welcome DocChat, the best wey to talk with your docs")

    # Initialize cat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "documents_to_search_in" not in st.session_state:
        st.session_state.documents_to_search_in = []
    if "documents_names_in_db" not in st.session_state:
        st.session_state.documents_names_in_db = []

    # Display chat messages from history on app rerun
    for n, message in enumerate(st.session_state.messages):
        if n % 2 == 0:
            st.divider()  # 👈 Draws a horizontal rule
        with st.container(border=True):
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input(
        "Hello there! How can I assist you today?",
    ):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        st.divider()
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            response = st.write_stream(response_generator(uri_service, prompt))
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
        # Register the conversation in the database
        register_memory(prompt, response, uri_service)

    with st.sidebar:
        st.write("This is the sidebar")
        docs = st.file_uploader(
            "Upload your file", accept_multiple_files=True, type=["pdf", "txt"]
        )

        if docs and st.button("Load docs"):
            with st.spinner("Loading docs"):

                documents_in_db = get_documents(uri_service)
                documents_in_db = pd.DataFrame(documents_in_db)

                if not documents_in_db.empty:
                    # ids to query the retriever
                    st.session_state.documents_to_search_in = documents_in_db["id"].tolist()
                    # names of the documents in the database
                    st.session_state.documents_names_in_db = documents_in_db["name"].tolist()
 
                # load the documents
                load_docs(
                    docs=docs,
                    uri_vs=uri_milvus,
                    uri_service=uri_service,
                    documents_in_bd=st.session_state.documents_names_in_db,
                )


if __name__ == "__main__":
    # change this variables to a config file
    # uri_service = "https://localhost:8080/" 
    uri_service = f"http://{os.getenv("BACKEND_HOST")}:{os.getenv("BACKED_PORT")}/"
    # uri_milvus = "/myapp/milvus_demo.db"
    uri_milvus = os.getenv("MILVUS_URI")
    main(uri_service, uri_milvus)
