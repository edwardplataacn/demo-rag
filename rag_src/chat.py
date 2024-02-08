# chat.py
# Facilitates user interaction with the AI assistant.

import streamlit as st
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from .model import initialize_models  # Adjust this import if necessary
from .vector_database import load_or_create_vector_database  # Updated import

# Initialize models
llm, document_embedder, query_embedder = initialize_models()

# Load or create the vector database
vectorstore = load_or_create_vector_database(force_rebuild=False)

def display_chat_ui():
    st.subheader("Chat with your AI Assistant, Envie!")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    user_input = st.text_input("Ask Envie a question:")

    if user_input:
        handle_user_input(user_input)

def handle_user_input(user_input):
    try:
        # Assuming vectorstore provides a method to retrieve relevant documents
        docs = vectorstore.get_relevant_documents(user_input)

        # Build context from retrieved documents
        context = "\n\n".join(doc["content"] for doc in docs)  # Adjust based on the actual structure of documents

        # Create augmented user input with context for the AI model
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful AI assistant named Envie. You will reply to questions only based on the context you are provided."),
            ("user", user_input)
        ])
        
        # Generate response using the language model
        response = llm.generate_response(prompt_template.construct_prompt(context))

        # Display response in the UI
        st.session_state.messages.append({"user": user_input, "envie": response})
        for message in st.session_state.messages:
            st.text_area("User", value=message["user"], height=100, key=message["user"][:10])
            st.text_area("Envie", value=message["envie"], height=100, key=message["envie"][:10])

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    display_chat_ui()
