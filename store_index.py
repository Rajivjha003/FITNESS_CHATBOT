from src.MEDICAL_CHATBOT.helper import load_pdf, text_split, download_hugging_face_embeddings
from pinecone import Pinecone
import pinecone
from dotenv import load_dotenv
import os

#load_dotenv()

PINECONE_API_KEY=os.environ.get("PINECONE_API_KEY")
PINECONE_API_ENV=os.environ.get("PINECONE_API_ENV")

#print("Environment variables loaded.")

extracted_data=load_pdf("E:\Medical_Chatbot\data")
print("PDF data loaded.")

text_chunks= text_split(extracted_data)
print("Text split into chunks.")

embeddings=download_hugging_face_embeddings()
print("Embeddings downloaded.")

pc = Pinecone(api_key=PINECONE_API_KEY)
print("Pinecone initialized.")

index_name="my-chatbot"

# Check if the index exists
if index_name in pc.list_indexes():
    pc.deindex(index_name)

# Create embeddings for each text chunk
vectors = embeddings.embed_documents([t.page_content for t in text_chunks])
print("Embeddings created for text chunks.")

# Upsert the embeddings into Pinecone
doc_ids = [f"{t.lc_id}_{i}" for i, t in enumerate(text_chunks)] 

items = [{"id": str(doc_id), "values": embedding} for doc_id, embedding in zip(doc_ids, vectors)]
index = pc.Index(name="my-chatbot")
index.upsert(vectors=items)

print("Embeddings upserted into Pinecone.")
