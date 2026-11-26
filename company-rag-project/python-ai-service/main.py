
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sentence_transformers import SentenceTransformer
from sqlalchemy import select

from database import SessionLocal
from models import DocumentChunk


app = FastAPI(
    title="Company Documentation AI",
    description="Python AI Microservice for RAG",
    version="1.0.0"
)


# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


# Request model
class SearchRequest(BaseModel):
    question: str
    top_k: int = Field(default=5, ge=1, le=20)


# Home API
@app.get("/")
def home():
    return {
        "message": "Company RAG AI Service is running!"
    }


# Health API
@app.get("/api/ai/health")
def health():
    return {
        "service": "Python AI Service",
        "status": "UP"
    }


# Semantic Search API
@app.post("/api/ai/search")
def search_documents(request: SearchRequest):

    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )

    # Convert question into embedding
    question_embedding = model.encode(question).tolist()

    db = SessionLocal()

    try:
        distance = DocumentChunk.embedding.cosine_distance(
            question_embedding
        )

        statement = (
            select(DocumentChunk, distance.label("distance"))
            .where(DocumentChunk.embedding.is_not(None))
            .order_by(distance)
            .limit(request.top_k)
        )

        rows = db.execute(statement).all()

        results = []

        for chunk, score in rows:
            results.append({
                "chunk_number": chunk.chunk_number,
                "content": chunk.chunk_text,
                "similarity": round(1 - score, 4)
            })

        return {
            "question": question,
            "total_results": len(results),
            "results": results
        }

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Error occurred during document search"
        )

    finally:
        db.close()
