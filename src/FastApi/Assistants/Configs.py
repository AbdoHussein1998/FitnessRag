# src/FastApi/Assistants/Config.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from ProjectAssetes import get_basic_settings
from ProjectAssetes import get_logger
import pymongo
async def connect_to_mongo(app: FastAPI):
    """
    Connect to MongoDB and set up the connection in the FastAPI app.
    """
    logger = get_logger(__name__)
    logger.info("Connecting to MongoDB...")
    basic_settings = get_basic_settings()
    app.mongo_conn = AsyncIOMotorClient(basic_settings.MongoDB_URL)
    app.mongo_db = app.mongo_conn[basic_settings.MongoDB_DB_NAME]
    app.mongo_collections_names = await app.mongo_db.list_collection_names()


    logger.info(f"Connected to MongoDB and database name is {basic_settings.MongoDB_DB_NAME}")
    if app.mongo_collections_names is not None:
        for collection_name in [basic_settings.MongoDB_COLLECTION_NAME_DR_MIKE,
                                basic_settings.MongoDB_COLLECTION_NAME_JEFF_NIPPARD,
                                basic_settings.MongoDB_COLLECTION_NAME_TOMAS_DELURE,]:

            if collection_name not in app.mongo_collections_names:
                logger.info(f"Collection {collection_name} does not exist. Creating it...")
                await app.mongo_db.create_collection(collection_name)
                await app.mongo_db[collection_name].create_indexes([
                        pymongo.IndexModel([("title", 1)], name="title_index", unique=True),
                        pymongo.IndexModel([("file_id", 1)], name="id_index", unique=True)])
                app.mongo_collections_names.append(collection_name)
                logger.info(f"Collection {collection_name} created.")
                for collection_name in [
                                        basic_settings.MongoDB_COLLECTION_NAME_CHUNKS,
                                        basic_settings.MongoDB_COLLECTION_NAME_CHUNKED_IDS,
                                        basic_settings.MongoDB_COLLECTION_NAME_EMBEDDED_CHUNKS,]:
                    if collection_name not in app.mongo_collections_names:      
                        logger.info(f"Collection {collection_name} does not exist. Creating it...") 
                        await app.mongo_db.create_collection(collection_name)
                        logger.info(f"Collection {collection_name} created.")

@asynccontextmanager
async def fastapi_lifespan(app: FastAPI):

    """
    Lifespan context manager for FastAPI to handle startup and shutdown events.
    """
    await connect_to_mongo(app)


    yield

    print("Shutting down...")