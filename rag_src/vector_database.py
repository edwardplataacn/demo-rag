 # rag_src/vector_database.py

import os
import pickle
from langchain.vectorstores import FAISS
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import CharacterTextSplitter
from .model import initialize_models  # Make sure this import matches your project structure
import streamlit as st

# Initialize models (ensure this is consistent with your actual model initialization)
_, document_embedder, _ = initialize_models()

DOCS_DIR = os.path.abspath("./uploaded_docs")  # Adjust based on your document storage directory
VECTOR_STORE_PATH = os.path.abspath("vectorstore.pkl")  # Path to save or load the vector store

def load_or_create_vector_database(force_rebuild=False):
    """
    Loads an existing vector database from file or creates a new one.
    
    Args:
        force_rebuild (bool): If True, forces the rebuild of the vector database even if it exists.
    
    Returns:
        FAISS vector store.
    """
    if os.path.exists(VECTOR_STORE_PATH) and not force_rebuild:
        with open(VECTOR_STORE_PATH, "rb") as f:
            vectorstore = pickle.load(f)
        st.success("Existing vector store loaded successfully.")
    else:
        vectorstore = create_vector_database()
        with open(VECTOR_STORE_PATH, "wb") as f:
            pickle.dump(vectorstore, f)
        st.success("Vector store created and saved.")
    return vectorstore

def create_vector_database():
    """
    Creates a new vector database by processing documents in the designated directory.
    
    Returns:
        FAISS vector store.
    """
    raw_documents = DirectoryLoader(DOCS_DIR).load()
    if not raw_documents:
        st.warning("No documents found in the directory.")
        return None

    text_splitter = CharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
    documents = text_splitter.split_documents(raw_documents)

    # Assuming document_embedder is a model that can produce embeddings for a batch of documents
    vectorstore = FAISS.from_documents(documents, document_embedder)
    
    return vectorstore
