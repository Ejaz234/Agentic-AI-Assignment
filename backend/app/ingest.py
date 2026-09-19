import os
from dotenv import load_dotenv
from pinecone import Pinecone
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()


loader = PyPDFLoader("data/Agentic-AI.pdf")
documents = loader.load()


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = text_splitter.split_documents(documents)

print(f"Total chunks: {len(chunks)}")


embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

index = pc.Index("agentic-ai")


vectors = []

for i, chunk in enumerate(chunks):
    vector = embeddings.embed_query(chunk.page_content)

    vectors.append({
        "id": f"chunk-{i}",
        "values": vector,
        "metadata": {
            "text": chunk.page_content,
            "page": chunk.metadata.get("page", 0) + 1,
            "source": "Agentic-AI.pdf"
        }
    })


index.upsert(vectors=vectors)

print(f"Successfully uploaded {len(vectors)} chunks to Pinecone!")