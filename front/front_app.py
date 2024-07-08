from cgitb import text
import tempfile
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from pathlib import Path
from tempfile import NamedTemporaryFile
from pypdf import PdfReader
from langchain_core.documents import Document


def pdf_to_docs(doc):
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
    print(len(chunks[0].page_content))
    return chunks


def create_collection(uri, collection_name, docs, embeddings):
    # Milvus.from_documents(
    #     documents=docs,
    #     embedding=embeddings,
    #     connection_args={
    #         "uri": uri,
    #     },
    #     collection_name=collection_name,
    #     drop_old=True,  # Drop the old Milvus collection if it exists
    # )
    pass    

def load_docs(docs, uri):
    list_data = []
    for doc in docs:
        # Get chunks for the document
        chunks_pdf = pdf_to_docs(doc)
        ## create a collection for the document
        # create_collection(uri, Path(doc.name).stem, chunks_pdf, OpenAIEmbeddings())
    return list_data



def main():
    st.set_page_config(
        page_title="Chat with your docs", page_icon=":green_book:", layout="wide"
    )
    st.title("DocChat App")
    st.header("Welcome DocChat, the best wey to talk with your docs")
    st.text_input("Enter your name", "John Doe")

    with st.sidebar:
        st.write("This is the sidebar")
        docs = st.file_uploader(
            "Upload your file", accept_multiple_files=True, type=["pdf", "txt"]
        )

        if docs and st.button("Load docs"):
            with st.spinner("Loading docs"):
                documents = load_docs(docs, uri="milvus_demo.db")
                st.write(documents)
                # get docs names from the database


if __name__ == "__main__":
    main()
