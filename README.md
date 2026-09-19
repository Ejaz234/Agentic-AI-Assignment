# Agentic AI RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot that answers questions strictly from the **Agentic AI eBook**.

## 🚀 Live Demo

- Frontend: https://agentic-ai-assignment-umber.vercel.app
- Backend API: https://agentic-ai-assignment-w2b2.onrender.com
- API Docs: https://agentic-ai-assignment-w2b2.onrender.com/docs

## 🛠️ Tech Stack

- **Frontend:** React, Vite
- **Backend:** FastAPI, Python
- **RAG:** LangGraph, LangChain
- **Embeddings:** FastEmbed (`BAAI/bge-small-en-v1.5`)
- **Vector DB:** Pinecone
- **LLM:** Groq (`openai/gpt-oss-120b`)
- **Document:** Agentic AI eBook PDF

## 🧠 Architecture

```text
Agentic AI PDF
     ↓
Text Chunking
     ↓
FastEmbed
     ↓
Pinecone
     ↓
User Question
     ↓
LangGraph
     ↓
Retrieve Top 3 Chunks
     ↓
Groq LLM
     ↓
Grounded Answer
     ↓
React Frontend
```

## ⚙️ Setup

Clone the repository and install the dependencies:

    git clone <YOUR_GITHUB_REPO_URL>
    cd Agentic-AI-Assignment

### Backend

    cd backend
    python -m venv venv

Windows:

    venv\Scripts\activate

Install dependencies:

    pip install -r requirements.txt

Create a `.env` file inside `backend`:

    GROQ_API_KEY=your_groq_api_key
    PINECONE_API_KEY=your_pinecone_api_key

Ingest the PDF:

    python app/ingest.py

Start the backend:

    python -m uvicorn main:app --reload

API: `http://127.0.0.1:8000`

Swagger Docs: `http://127.0.0.1:8000/docs`

### Frontend

    cd frontend
    npm install

Create `.env.local`:

    VITE_API_URL=http://127.0.0.1:8000

Run the frontend:

    npm run dev

## 💬 Sample Queries

1. What is Agentic AI?
2. What are the key characteristics of Agentic AI?
3. How is Agentic AI different from traditional AI?
4. What are multi-agent systems?
5. How do AI agents make decisions?
6. What are the challenges of Agentic AI?

### Out-of-Domain Test

Question: `What is the capital of France?`

Expected response:

`I could not find this information in the knowledge base.`

## 📊 Response

The chatbot returns the final answer, retrieved context, page numbers, and Pinecone similarity scores. The similarity score represents vector similarity and is not a confidence percentage.

## 📦 Deliverables

- GitHub Repository
- README with setup instructions
- Working RAG chatbot with Web UI and API
- 6 sample queries
- Short architecture explanation
- Deployed frontend and backend
