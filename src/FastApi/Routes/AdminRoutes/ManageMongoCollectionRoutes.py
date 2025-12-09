

import pymongo
from fastapi import APIRouter ,Request,Form,status
from ProjectAssetes import get_logger
from fastapi.responses import JSONResponse
from DataBase.Json.Provider.MongoDb import MongoDbCollectionController

create_collection_in_mongo_router=APIRouter()
@create_collection_in_mongo_router.post("/create-collection-in-mongo")
async def create_collection_in_mongo(request:Request,collection_name:str=Form(...)):

    #init class
    manage_obj=await MongoDbCollectionController.init_class(request=request)


    #create collection

    result=await manage_obj.create_collection(collection_name=collection_name)
    if result == True:
        return JSONResponse(status_code=status.HTTP_201_CREATED,content="Sucessfully Done")
    else:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content="Error In Creating Collection")


delete_collection_in_mongo_router=APIRouter()
@delete_collection_in_mongo_router.post("/delete-collection-in-mongo")
async def delete_collection_in_mongo(request:Request, collection_name:str=Form(...)):
    #init class
    manage_obj=await MongoDbCollectionController.init_class(request=request)
    #delete collection
    result=await manage_obj.delete_collection(collection_name=collection_name)
    if result == True:
        return JSONResponse(status_code=status.HTTP_200_OK,content="Sucessfully Done")
    else:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content="Error In Deleting Collection")

