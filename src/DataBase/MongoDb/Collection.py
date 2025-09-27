


from fastapi import Request

from ProjectAssetes import get_logger
import asyncio
from DataBase.DataBaseAssets import ConnectionsAssets
from flask import request

class MongoDbCollection(ConnectionsAssets):
    
    def __init__(self,request:Request,collection_name:str):
        super.__init__(request=request)
        self.logger = get_logger(__name__)
        self.collection = self.mongo_db[collection_name]
        
    
    
    @classmethod
    async def init_class(cls,request: Request,collection_name:str):
        instance=cls(request=request, collection_name=collection_name)
        await instance.init_class()
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
                self.logger.info(f"Document found: {result}")
                return (result,result.inserted_id)
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
            return (result, inserted_ids)
        

        
                



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


            





