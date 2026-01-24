# Medical Chatbot 🩺🤖

A RAG-based (Retrieval-Augmented Generation) medical AI assistant built with **Llama-3.1**, **LangChain**, and **FAISS**. This project allows users to ask medical questions and receive accurate answers derived strictly from your custom PDF medical data.

It features dual interfaces:
1. **Streamlit UI** for rapid prototyping and testing.
2. **FastAPI + Next.js** for a production-ready web application.

## 🚀 Features

* **RAG Architecture:** Retrieves relevant context from local PDF medical documents to prevent hallucinations.
* **High-Speed Inference:** Uses **Groq** API to run **Llama-3.1-8b-instant** with near-instant responses.
* **Vector Search:** Utilizes **FAISS** (Facebook AI Similarity Search) for efficient document retrieval.
* **Embeddings:** Powered by HuggingFace's `sentence-transformers/all-MiniLM-L6-v2`.
* **Modern Frontend:** A responsive web interface built with **Next.js 16** and **Tailwind CSS**.
* **API-First Design:** Fully functional REST API built with **FastAPI**.

---

## 📂 Project Structure


├── data/                       # Store your medical PDF documents here
├── vectorstore/                # Generated FAISS vector database stores here
├── frontend/                   # Next.js Frontend application
│   ├── app/                    # App router components
│   └── package.json            # Frontend dependencies
├── api.py                      # FastAPI backend for the web app
├── create-memory-for-llm.py    # Script to ingest PDFs and create vector store
├── medical-chatbot.py          # Streamlit UI application
├── connect-memory-with-llm.py  # CLI script for testing RAG chain
├── requirements.txt            # Python dependencies
└── .env                        # Environment variables (API Keys)

## 🛠️ Installation & Setup
Prerequisites
Python 3.9+

Node.js & npm (for the frontend)

A Groq API Key

## 1. Clone the Repository

git clone [https://github.com/miankhan-ai/medical-chatbot.git](https://github.com/miankhan-ai/medical-chatbot.git)
cd medical-chatbot

## 2. Backend Setup
Create a virtual environment and install dependencies:

## Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

## 3. Environment Configuration
Create a .env file in the root directory and add your API key:

GROQ_API_KEY=your_actual_groq_api_key_here

## 4. Frontend Setup
Navigate to the frontend folder and install dependencies:

cd frontend
npm install
cd ..

## 🧠 Step 1: Ingesting Data
Before running the bot, you must create the "memory" (Vector Store).

Place your medical PDF textbooks or documents inside the data/ folder.

Run the ingestion script:

python create-memory-for-llm.py

What this does: It loads PDFs, chunks the text, creates embeddings using HuggingFace, and saves the index to vectorstore/db_faiss.

## 🖥️ Step 2: Running the Application
You can run the project in two modes:

## Mode A: Streamlit (Quick UI)
Best for testing the model logic locally.

streamlit run medical-chatbot.py
Access the UI at http://localhost:8501.

Mode B: Full Web App (FastAPI + Next.js)
Best for production-style deployment.

## 1. Start the Backend API:


uvicorn api:app --host 0.0.0.0 --port 8000 --reload
The API will be live at http://localhost:8000.

Swagger docs available at http://localhost:8000/docs.

## 2. Start the Frontend: Open a new terminal, navigate to frontend, and run:

cd frontend
npm run dev
Access the web app at http://localhost:3000.

## 🧪 Testing via CLI
If you want to debug the retrieval chain without a UI:

python connect-memory-with-llm.py

## 🛡️ License
This project is licensed under the MIT License - see the LICENSE file for details.

⚠️ Disclaimer
For Educational Use Only. This chatbot provides information based on the provided documents. It is not a substitute for professional medical advice, diagnosis, or treatment.

