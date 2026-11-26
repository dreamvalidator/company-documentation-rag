
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
    func
)

from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector

from database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String(255), nullable=False)
    file_path = Column(Text, nullable=False)
    uploaded_by = Column(String(100), nullable=True)
    uploaded_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    chunks = relationship(
        "DocumentChunk",
        back_populates="document",
        cascade="all, delete-orphan"
    )


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(
        Integer,
        ForeignKey("documents.id", ondelete="CASCADE"),
        nullable=False
    )
    chunk_text = Column(Text, nullable=False)
    chunk_number = Column(Integer, nullable=False)
    embedding = Column(Vector(384), nullable=True)

    document = relationship(
        "Document",
        back_populates="chunks"
    )
