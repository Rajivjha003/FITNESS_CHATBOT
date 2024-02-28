from flask import Flask, render_template, jsonify, request
from src.MEDICAL_CHATBOT.helper import download_hugging_face_embeddings
from langchain_community.vectorstores import Pinecone
from pinecone import Pinecone
import pinecone
from langchain_pinecone import PineconeVectorStore
from langchain.prompts import PromptTemplate
from langchain_community.llms import CTransformers
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import chroma
from dotenv import load_dotenv
from src.MEDICAL_CHATBOT.prompt import *
import os
from pinecone import Config


app = Flask(__name__)

load_dotenv()

PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
PINECONE_API_ENV = os.environ.get('PINECONE_API_ENV')

embeddings = download_hugging_face_embeddings()

#Initializing the Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)

index_name="my-chatbot"

# Instantiate an Index object
docsearch = pc.Index(name=index_name)

text_field = "text"

vectorstore = PineconeVectorStore(docsearch, embeddings.embed_query, text_field)

PROMPT=PromptTemplate(template=prompt_template, input_variables=["context", "question"])

chain_type_kwargs={"prompt": PROMPT}

llm=CTransformers(model="model/llama-2-7b-chat.ggmlv3.q4_0.bin",
                  model_type="llama",
                  config={'max_new_tokens':512,
                          'temperature':0.8})

# Initialize the ConversationalRetrievalChain
qa = RetrievalQA.from_chain_type(
    llm=llm, 
    retriever=vectorstore.as_retriever(),
    return_source_documents=True, 
    chain_type_kwargs=chain_type_kwargs
)

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    print(input)
    result=qa({"query": input})
    print("Response : ", result["result"])
    return str(result["result"])

if __name__ == '__main__':
    app.run(host="0.0.0.0", port= 8080, debug= True)