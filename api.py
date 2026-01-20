# api.py
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# LangChain Imports
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv

# Load Environment Variables
load_dotenv()

app = FastAPI()

# Enable CORS (Crucial for Next.js to talk to Python)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In real production, set this to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Vector Store Global Variable
vectorstore = None
DB_FAISS_PATH = "vectorstore/db_faiss"

@app.on_event("startup")
async def load_vectorstore():
    global vectorstore
    embedding_model = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    if os.path.exists(DB_FAISS_PATH):
        vectorstore = FAISS.load_local(DB_FAISS_PATH, embedding_model, allow_dangerous_deserialization=True)
        print("✅ Vector Store Loaded Successfully!")
    else:
        print("❌ Vector Store Path Not Found!")

# Define Request Body Structure
class ChatRequest(BaseModel):
    query: str

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    if not vectorstore:
        raise HTTPException(status_code=500, detail="Vector store not initialized")
    
    try:
        # 1. Setup LLM (Groq)
        llm = ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0.5,
            max_tokens=512,
            api_key=os.environ.get("GROQ_API_KEY")
        )

        # 2. Setup Prompt
        # Note: We use {input} instead of {question} to match standard retrieval chains
        custom_prompt = """
        Use the pieces of information provided in the context to answer user's question.
        If you dont know the answer, just say that you dont know, dont try to make up an answer. 
        Dont provide anything out of the given context

        Context: {context}
        Question: {input}

        Start the answer directly. No small talk please.
        """
        
        prompt = PromptTemplate(template=custom_prompt, input_variables=["context", "input"])

        # 3. Create RAG Chain
        combine_docs_chain = create_stuff_documents_chain(llm, prompt)
        retriever = vectorstore.as_retriever(search_kwargs={'k': 3})
        rag_chain = create_retrieval_chain(retriever, combine_docs_chain)

        # 4. Generate Answer
        response = rag_chain.invoke({'input': request.query})
        
        return {"answer": response["answer"]}

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))