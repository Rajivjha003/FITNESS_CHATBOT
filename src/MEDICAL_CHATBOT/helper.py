# helper.py
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from pinecone import Pinecone  # Added import statement for Pinecone
from dotenv import load_dotenv
import os
from langchain.chains.retrieval_qa.base import BaseRetriever


load_dotenv()
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
PINECONE_API_ENV = os.environ.get("PINECONE_API_ENV")

# Extract the data from pdf
def load_pdf(data):
    loader = DirectoryLoader(data, glob="*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()
    return documents

# Create Text Chunks
def text_split(extracted_data):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
    text_chunks = text_splitter.split_documents(extracted_data)
    return text_chunks

# Download embedding model
def download_hugging_face_embeddings():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return embeddings

# Initialize Pinecone
def initialize_pinecone():
    pc = Pinecone(api_key=PINECONE_API_KEY)
    return pc

# Create index in Pinecone
def create_pinecone_index(pc, index_name):
    if index_name in pc.list_indexes():
        pc.deindex(index_name)

    return pc.Index(name=index_name)

# Upsert embeddings into Pinecone index
def upsert_embeddings(index, text_chunks, embeddings):
    vectors = embeddings.embed_documents([t.page_content for t in text_chunks])
    doc_ids = [f"{t.lc_id}_{i}" for i, t in enumerate(text_chunks)]
    items = [{"id": str(doc_id), "values": embedding} for doc_id, embedding in zip(doc_ids, vectors)]
    index.upsert(vectors=items)
