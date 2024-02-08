import sys
import os

from rag_src.document_loader import setup_document_loader
from rag_src.chat import display_chat_ui

def main():
    setup_document_loader()
    display_chat_ui()

if __name__ == "__main__":
    main()
