#src\FastApi\Schemas\ChunkDocumentSchemas.py

from pydantic import BaseModel
from typing import Optional

class ChunkDocumentRequestPayload(BaseModel):
    collection_name: str
    document_id: Optional[str] = None
    title: Optional[str] = None
    chunk_size: Optional[int] = None
    overlap_size: Optional[int] = None
class EmbeddDocumentRequestPayload(BaseModel):
    chunks_text_collection_name: str
    vector_db_collection_name: Optional[str] = None    
    vector_db_name: Optional[str] = None
    embedding_model: Optional[str] = None
class CreateVectorCollectionRequestPayload(BaseModel):
    collection_name: str
    distance: str
    vector_db_name: Optional[str] = None
    embedding_model: Optional[str] = None