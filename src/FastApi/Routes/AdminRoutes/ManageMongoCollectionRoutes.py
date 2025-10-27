

import pymongo
from fastapi import APIRouter ,Request,Form,status
from ProjectAssetes import get_logger
from fastapi.responses import JSONResponse
from DataBase.Json.Provider.MongoDb import MongoDbCollection

create_collection_in_mongo_router=APIRouter()
@create_collection_in_mongo_router.post("/create-collection-in-mongo")
async def create_collection_in_mongo(request:Request,collection_name:str=Form(...)):

    #init class
    manage_obj=await MongoDbCollection.init_class(request=request,collection_name=collection_name)
    #create collection
    result=await manage_obj.create_collection(collection_name=collection_name)
    return JSONResponse(status_code=result[0],content=result[1])



delete_collection_in_mongo_router=APIRouter()
@delete_collection_in_mongo_router.post("/delete-collection-in-mongo")
async def delete_collection_in_mongo(request:Request, collection_name:str=Form(...)):
    #init class
    manage_obj=await MongoDbCollection.init_class(request=request,collection_name=collection_name)
    #delete collection
    result=await manage_obj.delete_collection(collection_name=collection_name)
    return JSONResponse(status_code=result[0], content=result[1])
