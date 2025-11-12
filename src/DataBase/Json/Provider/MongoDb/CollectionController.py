



from fastapi import Request,status

from ProjectAssetes import get_logger
import asyncio
from DataBase.DataBaseAssets import ConnectionsAssets
import pymongo
from DataBase.Json.JsonInterface import CollectionControllerInterface
import pymongo
from motor.motor_asyncio import AsyncIOMotorCollection




class MongoDbCollectionController(ConnectionsAssets,CollectionControllerInterface):
    def __init__(self,request:Request,):
        super().__init__(request=request)
        self.logger = get_logger(__name__)
        self.all_collections=[]
        self.request=request


    async def connect(self,collection_name:str):
        result=await self.is_collection_existed(collection_name=collection_name)
        if result==True:
            self.logger.info(f"Connected to Collection {collection_name}")
            self.collection=self.request.app.mongo_db[collection_name]
            return True
        else: 
            self.logger.error(f"No Collection With this Name {collection_name}")
            return False
    
    async def list_collections(self)->list:

        collection_names=await self.request.app.mongo_db.list_collection_names()
        return collection_names
    
    async def is_collection_existed(self,collection_name:str)->bool:
        collection_names=await self.list_collections()
        if collection_name in collection_names:
            return True
        else: 
            return False
        
    @classmethod
    async def init_class(cls,request: Request):
        instance=cls(request=request)
        return instance
    
    async def insert_one(self,document:dict):

        print("we are insert_one")
        try:
            result= await self.collection.insert_one(document)
            return True,result.inserted_id
        except pymongo.errors.DuplicateKeyError:
            self.logger.error(f"Document with file_id {document['file_id']} already exists.")
            return False,pymongo.errors.DuplicateKeyError
        except Exception as e:
            self.logger.error(f"Error inserting document: {e}")
            return False,e
        
    async def insert_many(self,documents:list[dict],batch_size:int=1000)->list:
            try:
                inserted_ids=[]
                for i in range(0,len(documents),batch_size):
                    batch=documents[i:i+batch_size]
                    result= await self.collection.insert_many(batch)
                    inserted_ids.extend(result.inserted_ids)
                    self.logger.info(f"We sucssufly inserted {len(inserted_ids)} / {len(documents)} ")
                    await asyncio.sleep(0.1)
                return True,inserted_ids
            except Exception as e:
                self.logger.error(f"Error inserting document: {type(e).__name__}: {str(e)[:200]}")  # Limit to 200 chars
                return False,inserted_ids

    async def find_one(self,filter_dict:dict)->tuple:    

            try:
                document=await self.collection.find_one(filter_dict)
                if document:
                    return True,document
                else:
                    self.logger.error(f"Document not found.")
                    return False,None
            except Exception as e:
                self.logger.error(f"Error finding document: {e}")
                return False,None

    async def stream_many_as_batches(self,filter_dict:dict=None,projection=None,batch_size:int=1000,)->list[dict]:

            if not filter_dict:
                filter_dict = {}

            batch=[] 
            counter=0


            cursor=self.collection.find(filter_dict,projection)

            async for document in cursor:
                    batch.append(document)
                    if len(batch) == batch_size:
                        counter+=len(batch)
                        yield batch
                        batch=[]
                        print(f"we have {counter} documents")
                        await asyncio.sleep(2)

                        
            if batch:
                counter+=len(batch)
                yield batch
                print(f"final bacth we have  {counter} documents")

   
    async def create_collection(self, collection_name: str) -> bool:
        
        try:
            is_existed = await self.is_collection_existed(collection_name)
            if is_existed:
                self.logger.warning(f"Collection '{collection_name}' already exists.")
                return True
            else:
                self.logger.info(f"Creating collection '{collection_name}'...")
                await self.request.app.mongo_db.create_collection(collection_name)
                self.logger.info(f"Collection '{collection_name}' created successfully.")
                self.logger.info(f"Creating indexes for collection '{collection_name}'...")
                new_collection=self.request.app.mongo_db[collection_name]
                index_models = [
                    pymongo.IndexModel([("title", 1)], name="title_index", unique=True),
                    pymongo.IndexModel([("file_id", 1)], name="id_index", unique=True)
                ]
                
                # create_indexes() is async-safe in Motor
                index_names = await new_collection.create_indexes(index_models)
                self.logger.info(f"Indexes created for collection '{collection_name}': {index_names}")
                
                return True
        except Exception as e:
            self.logger.error(f"Error creating collection '{collection_name}': {e}")
            return False
        

    async def delete_collection(self, collection_name: str) -> bool:
        try:
            is_existed = await self.is_collection_existed(collection_name)
            if not is_existed:
                self.logger.warning(f"Collection '{collection_name}' does not exist.")
                return False

            mongo_db = self.request.app.mongo_db
            await mongo_db.drop_collection(collection_name)
            self.logger.info(f"Collection '{collection_name}' deleted successfully.")
            return True

        except Exception as e:
            self.logger.error(f"Error deleting collection '{collection_name}': {e}")
            return False


    

    async def find_many():
        pass
    

    async def disconnect(self):
        pass
