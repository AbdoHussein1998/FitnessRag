#src\DataBase\VectorDB\Providers\QdrantDb.py

from qdrant_client import AsyncQdrantClient 
from qdrant_client.models import VectorParams
from ProjectAssetes import get_basic_settings 
from ProjectAssetes import get_logger   

class QdrantDbProvider:
    def __init__(self):
        
        self.basic_setting = get_basic_settings()
        self.logger = get_logger(__name__) 
        self.client=AsyncQdrantClient(
            api_key=self.basic_setting.QDRANT_DB_API_KEY,
            url=self.basic_setting.QDRANT_DB_URL
        )
        self.logger.info(f"Qdrant DB Provider is iniszlized")
    



    async def connect(self,collection_name):
        self.logger.info(f"Connected to Qdrant DB ...")
        case=self.is_collection_existed(collection_name)
        if case==True:
            self.collection=self.client.get_collection(collection_name)
            self.logger.info(f"Connected to collection {collection_name}")
            return True
        else:
            self.logger.error(f"Collection {collection_name} does not exist, \n please create it first")
            return False
        
    async def disconnect(self):
        self.client=None

    async def list_all_collections(self) -> list:
        collections = await self.client.get_collections()  
        self.all_qdrant_db_collections_names = [x.name for x in collections.collections]        
        return self.all_qdrant_db_collections_names
    
    async def is_collection_existed(self, collection_name: str) -> bool:
        if collection_name in await self.list_all_collections():
            self.logger.info(f"Collection {collection_name} is existed")
            return True
        else:
            self.logger.info(f"Collection {collection_name} is not existed")
            return False
    

    async def get_collection_info(self, collection_name: str) -> dict:
        if await self.is_collection_existed(collection_name)==True:
            col = await self.client.get_collection(collection_name)
            return dict(col.config)

    async def delete_collection(self, collection_name: str):
        if await self.is_collection_existed(collection_name)==True:
            try:
                self.logger.info(f"Deleting collection {collection_name}....")
                await self.client.delete_collection(collection_name)
                self.logger.info(f"Collection {collection_name} is deleted")
                return True
            except Exception as e:
                self.logger.error(f"Error deleting collection: {e}")
                return False
            

    async def create_collection(self, collection_name: str, vector_dimension: int,distance:str):
            if await self.is_collection_existed(collection_name)==False:
                try:
                    self.logger.info(f"Creating collection {collection_name}....")
                    await self.client.create_collection(collection_name=collection_name,
                                                        vector_size=vector_dimension,distance= distance)
                                                    
                    self.logger.info(f"Collection {collection_name} created")
                    return True
                except Exception as e:
                    self.logger.error(f"Error creating collection: {e}")
                    return False
                
    async def delete_collection(self,collection_name:str):
        if await self.is_collection_existed(collection_name)==True:
            try:
                self.logger.info(f"Deleting collection {collection_name}....")
                await self.client.delete_collection(collection_name)
                self.logger.info(f"Collection {collection_name} is deleted")
                return True
            except Exception as e:
                self.logger.error(f"Error deleting collection: {e}")
                return False
            
    async def insert_one(self, collection_name: str,
                         text: str,
                         vector: list,
                         metadata: dict = None, 
                         record_id: str = None):
            pass
        
    #     if await self.is_collection_existed(collection_name)==False:
    #         self.logger.error(f"Collection {collection_name} does not exist,\n please create it first")
    #         try: 
    #             self.client.upload_records(
    #                 collection_name=collection_name,
    #                 records=[
    #                     async_qdrant_client.Record(
    #                         id=record_id,
    #                         vector=vector,
    #                         payload={
    #                             "text": text,
    #                             "metadata": metadata
    #                         }
    #                     )
    #                 ]
    #             )
    #         except Exception as e:
    #             self.logger.error(f"Error inserting record: {e}")
                
    # async def insert_many(self, collection_name: str, texts: list, 
    #                       vectors: list, metadata: list = None, 
    #                       record_ids: list = None, batch_size: int = 50):
    #     pass

    # async def search_by_vector(self, collection_name: str, vector: list, limit: int):
    #     pass
