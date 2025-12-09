#src\DataBase\VectorDB\Controller\QdrantDBController.py
from ProjectAssetes import get_logger,get_basic_settings
from qdrant_client.http.models import PointStruct
import uuid

class QdrantDbPreProcessing:
    def __init__(self):
        self.basic_setting = get_basic_settings()
        self.logger = get_logger()

    def create_payload(self,document:dict)->dict:
        payload = {
            "text": document["text"],
            "title": document["title"],
            "file_id":document["file_id"],
            "mongo_id":document["mongo_id"],
        }
        return payload
    
    def create_point_struct(self, vector: list, payload: dict)->dict:
        point_struct = PointStruct(
            id=str(uuid.uuid4()),
            vector=vector,
            payload=payload
        )
        return point_struct
    
