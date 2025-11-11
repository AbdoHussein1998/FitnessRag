#src\DataBase\VectorDB\Providers\QdrantDb.py

from qdrant_client import async_qdrant_client
from ProjectAssetes import get_basic_settings 
from ProjectAssetes import get_logger   

class QdrantDbProvider:
    def __init__(self):
        self.basic_setting = get_basic_settings()
        self.logger = get_logger()

    async def connect(self):
        self.client=async_qdrant_client(
            api_key=self.basic_setting.QDRANT_DB_API_KEY,
            url=self.basic_setting.QDRANT_DB_URL
        )
        self.collections=await self.client.get_collections()
    

    async def disconnect(self):
        self.client=None

    async def list_all_collections(self) -> list:
        return self.collections
    async def is_collection_existed(self, collection_name: str) -> bool:
        if collection_name in self.collections:
            self.logger.info(f"Collection {collection_name} already exists")
            return True
        else:
            self.logger.info(f"Collection {collection_name} does not exist")
            return False
        


    async def get_collection_info(self, collection_name: str) -> dict:
        if await self.is_collection_existed(collection_name)==True:
            return await self.client.get_collection(collection_name)
    

    async def delete_collection(self, collection_name: str):
        if await self.is_collection_existed(collection_name)==True:
            await self.client.delete_collection(collection_name)
            self.logger.info(f"Collection {collection_name} deleted")

    async def create_collection(self, collection_name: str, 
                                embedding_size: int,
                                ):
        
            if await self.is_collection_existed(collection_name)==False:
                self.logger.info(f"Creating collection {collection_name}....")
                try:
                    await self.client.create_collection(
                        collection_name=collection_name,
                        vectors_config=async_qdrant_client.VectorsConfig(
                            size=embedding_size,
                            distance=async_qdrant_client.Distance
                        )
                    )
                    self.logger.info(f"Collection {collection_name} created")
                except Exception as e:
                    self.logger.error(f"Error creating collection: {e}")

    async def insert_one(self, collection_name: str,
                         text: str,
                         vector: list,
                         metadata: dict = None, 
                         record_id: str = None):
        
        if await self.is_collection_existed(collection_name)==False:
            self.logger.error(f"Collection {collection_name} does not exist,\n please create it first")
            try: 
                self.client.upload_records(
                    collection_name=collection_name,
                    records=[
                        async_qdrant_client.Record(
                            id=record_id,
                            vector=vector,
                            payload={
                                "text": text,
                                "metadata": metadata
                            }
                        )
                    ]
                )
            except Exception as e:
                self.logger.error(f"Error inserting record: {e}")
                
    async def insert_many(self, collection_name: str, texts: list, 
                          vectors: list, metadata: list = None, 
                          record_ids: list = None, batch_size: int = 50):
        pass

    async def search_by_vector(self, collection_name: str, vector: list, limit: int):
        pass
