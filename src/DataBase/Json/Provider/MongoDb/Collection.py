


from fastapi import Request,status

from ProjectAssetes import get_logger
import asyncio
from DataBase.DataBaseAssets import ConnectionsAssets
import pymongo
from DataBase.Json.JsonInterface import CollectionController


class MongoDbCollection(ConnectionsAssets,CollectionController):
    def __init__(self,request:Request,collection_name:str):
        super().__init__(request=request)
        self.logger = get_logger(__name__)
        self.collection = self.mongo_db[collection_name]

    @classmethod
    async def init_class(cls,request: Request,collection_name:str):
        instance=cls(request=request, collection_name=collection_name)
        return instance

    async def insert_one(self,document:dict)->tuple:
        try:
            result= await self.collection.insert_one(document)
            self.logger.info(f"Document inserted successfully: {result.inserted_id}")
            return (result,result.inserted_id)
        except Exception as e:
            self.logger.error(f"Error inserting document: {e}")
            return None
            
    async def find_one(self,filter_dict:dict)->tuple:
        try:
            result = await self.collection.find_one(filter=filter_dict)
            if result:
                self.logger.info(f"Document found: {result['title']}")
                return result
            else:
                self.logger.info("Document not found")
                return None
        except Exception as e:
            self.logger.error(f"Error finding document: {e}")
            return None

    async def insert_many(self,documents:list[dict],batch_size:int=1000)->list:
        try:
            inserted_ids=[]
            for i in range(0,len(documents),batch_size):
                batch=documents[i:i+batch_size]
                result= await self.collection.insert_many(batch)
                inserted_ids.extend(result.inserted_ids)
                self.logger.info(f"We sucssufly inserted {len(inserted_ids)} / {len(documents)} ")
                await asyncio.sleep(0.1)
            return inserted_ids


        except Exception as e:
            self.logger.error(f"Error inserting documents: {e}")
            return None

    async def find_many(self,filter_dict:dict=None,batch_size:int=1000)->list[dict]:
        all_docs=[]
        async for batch in self.stream_many_as_batches(filter_dict=filter_dict, batch_size=batch_size):
            all_docs.extend(batch)
            print(f"we got the {len(all_docs)} documents")
        return all_docs

    async def stream_many_as_batches(self,filter_dict:dict=None,batch_size:int=1000)->list[dict]:

            if not filter_dict:
                filter_dict = {}

            batch=[] 
            counter=0
            cursor=self.collection.find(filter=filter_dict)

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


        
    async def create_collection(self,collection_name:str):
        
        try:
            if collection_name in self.request.app.mongo_collections_names:
                return (status.HTTP_409_CONFLICT,f"Collection {collection_name} already exists.")
            else:
                # Creating the Collection and Indexing
                self.logger.info(f"Collection {collection_name} does not exist. Creating it...")
                await self.request.app.mongo_db.create_collection(collection_name)
                self.logger.info(f"Collection {collection_name} created.")
                await self.request.app.mongo_db[collection_name].create_indexes([
                        pymongo.IndexModel([("title", 1)], name="title_index", unique=True),
                        pymongo.IndexModel([("file_id", 1)], name="id_index", unique=True)])
                self.logger.info(f"Indexes created for collection {collection_name}.")
                self.request.app.mongo_collections_names.append(collection_name)
                self.logger.info(f"Collection {collection_name} created and indexed.")
                return (status.HTTP_201_CREATED,f"Collection {collection_name} created and indexed.")
        
        
        except Exception as e:
            self.logger.error(f"Error creating collection {collection_name}: {e}")
            return (status.HTTP_500_INTERNAL_SERVER_ERROR,f"Error creating collection {collection_name}: {e}")

    async def delete_collection(self, collection_name:str):

        try:
            if collection_name not in self.request.app.mongo_collections_names:
                return (status.HTTP_404_NOT_FOUND, f"Collection {collection_name} does not exist.")
            else:
                # Deleting the Collection and Indexing
                self.logger.info(f"Collection {collection_name} exists. Deleting it...")
                await self.request.app.mongo_db.drop_collection(collection_name)
                self.logger.info(f"Collection {collection_name} deleted.")
                self.request.app.mongo_collections_names.remove(collection_name)
                self.logger.info(f"Collection {collection_name} deleted.")
                return (status.HTTP_200_OK, f"Collection {collection_name} deleted.")

        except Exception as e:
            self.logger.error(f"Error deleting collection {collection_name}: {e}")
            return (status.HTTP_500_INTERNAL_SERVER_ERROR, f"Error deleting collection {collection_name}: {e}")

    





