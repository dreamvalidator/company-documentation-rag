
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Document, DocumentChunk


# 1. Load PDF
pdf_path = "documents/hr-policy.pdf"

reader = PdfReader(pdf_path)

full_text = ""

for page in reader.pages:
    text = page.extract_text()
    if text:
        full_text += text + "\n"


# 2. Split text into chunks
chunk_size = 500
overlap = 50

chunks = []
start = 0

while start < len(full_text):
    end = start + chunk_size
    chunk = full_text[start:end].strip()

    if chunk:
        chunks.append(chunk)

    start += chunk_size - overlap

print("Total Chunks:", len(chunks))


# 3. Generate embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")

embeddings = model.encode(chunks)

print("Embeddings Generated:", len(embeddings))


# 4. Save document and chunks in PostgreSQL
db: Session = SessionLocal()

try:
    document = Document(
        file_name="hr-policy.pdf",
        file_path=pdf_path,
        uploaded_by="admin"
    )

    db.add(document)
    db.flush()

    for index, chunk in enumerate(chunks, start=1):
        db_chunk = DocumentChunk(
            document_id=document.id,
            chunk_text=chunk,
            chunk_number=index,
            embedding=embeddings[index - 1].tolist()
        )

        db.add(db_chunk)

    db.commit()

    print("Document and chunks saved successfully!")
    print("Document ID:", document.id)

except Exception:
    db.rollback()
    raise

finally:
    db.close()
