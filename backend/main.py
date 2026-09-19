from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.graph import graph


app = FastAPI(title="Agentic AI RAG Chatbot")


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    question: str


@app.get("/")
def root():
    return {"message": "Agentic AI RAG Chatbot is running"}


@app.post("/chat")
def chat(request: ChatRequest):

    result = graph.invoke({
        "question": request.question,
        "context": [],
        "answer": "",
        "score": 0.0
    })

    return {
        "answer": result["answer"],
        "retrieved_context": result["context"],
        "score": result["score"]
    }