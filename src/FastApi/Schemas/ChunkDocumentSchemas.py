#src\FastApi\Schemas\ChunkDocumentSchemas.py

from pydantic import BaseModel
from typing import Optional

class ChunkDocumentRequestPayload(BaseModel):
    collection_name: str
    document_id: Optional[str] = None
    title: Optional[str] = None
