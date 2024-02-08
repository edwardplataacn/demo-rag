# document_loader.py
# Handles uploading documents to the knowledge base.

import os
import streamlit as st

def setup_document_loader():
    DOCS_DIR = os.path.abspath("./uploaded_docs")
    if not os.path.exists(DOCS_DIR):
        os.makedirs(DOCS_DIR)
    with st.sidebar:
        st.subheader("Add to the Knowledge Base")
        with st.form("my-form", clear_on_submit=True):
            uploaded_files = st.file_uploader("Upload a file:", accept_multiple_files=True)
            submitted = st.form_submit_button("Upload")
        if uploaded_files and submitted:
            for uploaded_file in uploaded_files:
                try:
                    with open(os.path.join(DOCS_DIR, uploaded_file.name), "wb") as f:
                        f.write(uploaded_file.read())
                    st.success(f"File {uploaded_file.name} uploaded successfully!")
                except Exception as e:
                    st.error(f"Failed to upload {uploaded_file.name}: {str(e)}")
