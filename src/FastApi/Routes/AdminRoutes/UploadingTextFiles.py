from FastApi.Assistants import UploadFileValidation

from DataBase.TEXT import TextProcessing
from fastapi import APIRouter, status,UploadFile,File,Form,Request
from fastapi.responses import JSONResponse
from DataBase.Json.Provider.MongoDb import MongoDbCollectionController



upload_text_file_router = APIRouter()
@upload_text_file_router.post("/upload-text-file")
async def upload_text_file(request:Request,
                           collection_name:str=Form(...),
                           file: UploadFile=File(...),
                           title:str=Form(...)):

    #Initaliztion 
    mcol=await MongoDbCollectionController.init_class(request=request)
    txt=TextProcessing(file=file)
    val=UploadFileValidation()
    

    # Connection
    await mcol.connect(collection_name=collection_name)

    # Validation
    if val.check_collection_name(collection_name,request) ==False:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=f"Collection name is not valid!, please provide the name of one of the follwing {request.app.mongo_collections_names}")
 
    if val.check_file_format(file,".txt") ==False:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content="File format is not supported!"
        )
    if val.check_file_size(file) ==False:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content="File size is too large!"
        )
    
    # Processing  
    document=txt.text_into_dict(collection_name=collection_name,title=title)
    
    
    #Upload the Text to Mongo 
    try:
        inserted_id= await mcol.insert_one(document=document,collection_name=collection_name)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "Text file uploaded successfully!",
                "title": title,
                "inserted_id": str(inserted_id[0]),
                "file_id": document["file_id"]
            }
        )

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=f"Error inserting documents: check logging for more info"
        )













 




