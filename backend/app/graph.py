import os
from typing import TypedDict

from dotenv import load_dotenv
from pinecone import Pinecone
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END

load_dotenv()


# 1. Define Graph State


class RAGState(TypedDict):
    question: str
    context: list
    answer: str
    score: float



# 2. Initialize Embeddings


embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)



# 3. Connect to Pinecone


pc = Pinecone(
    api_key=os.getenv("PINECONE_API_KEY")
)

index = pc.Index("agentic-ai")



# 4. Initialize Groq


llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)



# 5. Similarity Threshold


SIMILARITY_THRESHOLD = 0.3


# 6. Retrieve Node


def retrieve(state: RAGState):

    question = state["question"]

    # Convert question into embedding
    query_vector = embeddings.embed_query(question)

    # Search Pinecone
    results = index.query(
        vector=query_vector,
        top_k=3,
        include_metadata=True
    )

    matches = results["matches"]

    # No results found
    if not matches:
        return {
            "context": [],
            "score": 0.0
        }

    # Highest similarity score
    score = matches[0]["score"]

    # Reject irrelevant questions
    if score < SIMILARITY_THRESHOLD:
        return {
            "context": [],
            "score": score
        }

    # Build context
    context = []

    for match in matches:
        context.append({
            "text": match["metadata"]["text"],
            "page": match["metadata"]["page"],
            "score": match["score"]
        })

    return {
        "context": context,
        "score": score
    }



# 7. Generate Node


def generate(state: RAGState):

    question = state["question"]
    context = state["context"]

    # If no relevant context was found
    if not context:
        return {
            "answer": "I could not find this information in the knowledge base."
        }

    # Combine retrieved chunks
    context_text = "\n\n".join(
        f"[Page {item['page']}]\n{item['text']}"
        for item in context
    )

    prompt = f"""
You are an AI assistant answering questions strictly
from the Agentic AI eBook.

Use ONLY the information provided in the context below.

Do not use outside knowledge.
Do not make up information.

If the answer cannot be found in the provided context,
say exactly:

"I could not find this information in the knowledge base."

Context:
{context_text}

Question:
{question}

Answer:
"""

    response = llm.invoke(prompt)

    return {
        "answer": response.content
    }



# 8. Build LangGraph


graph_builder = StateGraph(RAGState)

graph_builder.add_node("retrieve", retrieve)
graph_builder.add_node("generate", generate)

graph_builder.add_edge(START, "retrieve")
graph_builder.add_edge("retrieve", "generate")
graph_builder.add_edge("generate", END)

graph = graph_builder.compile()



# 9. Test the Graph


if __name__ == "__main__":

    question = "What is Agentic AI?"

    result = graph.invoke({
        "question": question,
        "context": [],
        "answer": "",
        "score": 0.0
    })

    print("\nAnswer:")
    print(result["answer"])

    print("\nScore:")
    print(result["score"])

    print("\nRetrieved Context:")

    for item in result["context"]:
        print(f"\nPage: {item['page']}")
        print(f"Score: {item['score']}")
        print(item["text"])