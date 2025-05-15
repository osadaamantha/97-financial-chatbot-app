from fastapi import FastAPI
from pydantic import BaseModel
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv
import os
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()

# Add this block to enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific origin in production
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load existing vector store
CHROMA_DB_DIR = os.path.join(os.path.dirname(__file__), "chroma_db")
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectordb = Chroma(persist_directory=CHROMA_DB_DIR, embedding_function=embeddings)
retriever = vectordb.as_retriever(search_kwargs={"k": 3})

qa_chain = ConversationalRetrievalChain.from_llm(
    ChatOpenAI(model="gpt-4-turbo", temperature=0),
    retriever=retriever
)

# Define request model
class Question(BaseModel):
    question: str

# API endpoint
@app.post("/chat")
async def chat(q: Question):
    response = qa_chain({"question": q.question, "chat_history": []})
    return {"answer": response["answer"]}




