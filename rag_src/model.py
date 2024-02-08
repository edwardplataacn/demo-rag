# model.py
# Manages interactions with NVIDIA AI models.

from langchain_nvidia_ai_endpoints import ChatNVIDIA, NVIDIAEmbeddings
import dotenv
import os

dotenv.load_dotenv()

def initialize_models():
    os.environ['NVIDIA_API_KEY'] = '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'
    llm = ChatNVIDIA(model="mixtral_8x7b")
    document_embedder = NVIDIAEmbeddings(model="nvolveqa_40k", model_type="passage")
    query_embedder = NVIDIAEmbeddings(model="nvolveqa_40k", model_type="query")
    return llm, document_embedder, query_embedder
