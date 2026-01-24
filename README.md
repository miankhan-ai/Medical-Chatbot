# 🩺 Medical Chatbot 🤖

A **RAG-based (Retrieval-Augmented Generation) medical AI assistant** built with **Llama 3.1**, **LangChain**, and **FAISS**. This project enables users to ask medical questions and receive answers derived **strictly from custom medical PDF data**, reducing hallucinations and improving reliability.

The project supports **two interfaces**:

* **Streamlit UI** for rapid prototyping and testing
* **FastAPI + Next.js** for a production-ready web application

---

## 🚀 Features

* **RAG Architecture**: Retrieves relevant context from local PDF medical documents to prevent hallucinations
* **High-Speed Inference**: Uses Groq API with `llama-3.1-8b-instant` for near-instant responses
* **Vector Search**: FAISS (Facebook AI Similarity Search) for efficient document retrieval
* **Embeddings**: HuggingFace `sentence-transformers/all-MiniLM-L6-v2`
* **Modern Frontend**: Responsive UI built with Next.js 16 and Tailwind CSS
* **API-First Design**: Fully functional REST API using FastAPI

---

## 📂 Project Structure

```
medical-chatbot/
├── data/                         # Medical PDF documents
├── vectorstore/                  # Generated FAISS vector database
├── frontend/                     # Next.js frontend application
│   ├── app/                      # App router components
│   └── package.json              # Frontend dependencies
├── api.py                        # FastAPI backend
├── create-memory-for-llm.py      # PDF ingestion & vector store creation
├── medical-chatbot.py            # Streamlit UI application
├── connect-memory-with-llm.py    # CLI-based RAG testing
├── requirements.txt              # Python dependencies
├── .env                          # Environment variables
└── README.md
```

---

## 🛠️ Installation & Setup

### Prerequisites

* Python 3.9+
* Node.js & npm
* Groq API Key

---

## 1️⃣ Clone the Repository

```
git clone https://github.com/miankhan-ai/medical-chatbot.git
cd medical-chatbot
```

---

## 2️⃣ Backend Setup

### Create and Activate Virtual Environment

```
python -m venv venv
```

**Activate the environment**

Windows:

```
venv\Scripts\activate
```

macOS / Linux:

```
source venv/bin/activate
```

### Install Dependencies

```
pip install -r requirements.txt
```

---

## 3️⃣ Environment Configuration

Create a `.env` file in the root directory:

```
GROQ_API_KEY=your_actual_groq_api_key_here
```

---

## 4️⃣ Frontend Setup

```
cd frontend
npm install
cd ..
```

---

## 🧠 Step 1: Ingest Medical Data

Before running the chatbot, you must generate the vector store.

1. Place your medical PDF documents inside the `data/` directory
2. Run the ingestion script:

```
python create-memory-for-llm.py
```

### What This Does

* Loads and parses PDFs
* Splits text into chunks
* Generates embeddings using HuggingFace
* Stores vectors in `vectorstore/db_faiss`

---

## 🖥️ Step 2: Running the Application

You can run the project in **two modes**.

---

### 🔹 Mode A: Streamlit (Quick UI)

Best for local testing and rapid iteration.

```
streamlit run medical-chatbot.py
```

Access the UI at:

```
http://localhost:8501
```

---

### 🔹 Mode B: Full Web App (FastAPI + Next.js)

Best for production-style deployment.

#### 1. Start the Backend API

```
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

API available at:

```
http://localhost:8000
```

Swagger Docs:

```
http://localhost:8000/docs
```

#### 2. Start the Frontend

```
cd frontend
npm run dev
```

Access the web app at:

```
http://localhost:3000
```

---

## 🧪 CLI Testing (Optional)

To test the retrieval chain without a UI:

```
python connect-memory-with-llm.py
```

---

## 🛡️ License

This project is licensed under the **MIT License**. See the `LICENSE` file for details.

---

## ⚠️ Disclaimer

**For educational use only.**

This chatbot provides information strictly based on the supplied documents and is **not a substitute for professional medical advice, diagnosis, or treatment**.
