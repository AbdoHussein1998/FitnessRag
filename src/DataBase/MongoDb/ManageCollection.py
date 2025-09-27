


from DataBase.DataBaseAssets import ConnectionsAssets
from ProjectAssetes import get_logger
from fastapi import Request,status
from fastapi.responses import JSONResponse
import pymongo
import asyncio


class ManageCollection(ConnectionsAssets):
    def __init__(self,request:Request):
        super().__init__(request=request)
        self.logger=get_logger(__name__)
        

    @classmethod
    async def init_class(cls,request:Request):
        instance = cls(request=request)
        return instance
    
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
                        pymongo.IndexModel([("id", 1)], name="id_index", unique=True)])
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

