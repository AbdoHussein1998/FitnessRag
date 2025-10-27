#scr/DataBase/MongoDB/Chunks.py

from fastapi import Request
from DataBase.DataBaseAssets import ConnectionsAssets
from ProjectAssetes import get_logger



class ChunksManager:
    
    def __init__(self,chunk_size=1500,overlap=200):
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.logger = get_logger("ChunksManager")
    @classmethod
    async def init_class(cls,chunk_size=1000, overlap=200):
        instance=cls(chunk_size=chunk_size, overlap=overlap)
        return instance
    
    
   
    async def chunk_text(self, docs: list):
        """Async generator that yields all chunks for each document"""
        for doc in docs:
            self.logger.info(f"we are chunking {doc['title']}")
            chunks = []
            text = doc["text"]
            start = 0
            
            while start < len(text):
                end = start + self.chunk_size
                chunks.append(text[start:end])
                start = end - self.overlap if end < len(text) else end
            chunks=await self.process_chunked_text(chunks, doc["file_id"], doc["_id"],title=doc["title"])
            yield chunks  # Yield the complete list of chunks for this document


    async def process_chunked_text(self,chunks:list,file_id,mongo_id,title)->list[dict]:
        chunks_dic_list = []
        for i, chunk in enumerate(chunks):
            doc = {
                "mongo_id": str(mongo_id),
                "file_id": file_id,
                "chunk_id": i,
                "title":title,
                "text": chunk,
            }
            chunks_dic_list.append(doc)        
        return chunks_dic_list
    

    

