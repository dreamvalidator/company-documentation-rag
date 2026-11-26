
from sentence_transformers import SentenceTransformer
from sqlalchemy import select

from database import SessionLocal
from models import DocumentChunk


# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


def search_documents(question, top_k=5):

    # Convert question into a 384-dimensional vector
    question_embedding = model.encode(question).tolist()

    db = SessionLocal()

    try:
        # Find the 5 most similar chunks
        statement = (
            select(DocumentChunk)
            .order_by(
                DocumentChunk.embedding.cosine_distance(
                    question_embedding
                )
            )
            .limit(top_k)
        )

        results = db.execute(statement).scalars().all()

        print("\nQuestion:", question)
        print("\nRelevant Results:")

        for result in results:
            print("\n------------------------------")
            print("Chunk Number:", result.chunk_number)
            print("Content:", result.chunk_text)

    finally:
        db.close()


if __name__ == "__main__":

    question = input("Ask a question about the company: ")

    search_documents(question)
