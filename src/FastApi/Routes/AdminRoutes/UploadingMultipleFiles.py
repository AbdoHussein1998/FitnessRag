

from typing import List
from FastApi.Assistants import UploadFileValidation

from DataBase.TEXT import TextProcessing
from fastapi import APIRouter, status,UploadFile,File,Form,Request
from fastapi.responses import JSONResponse
from DataBase.Json.Provider.MongoDb import MongoDbCollectionController



upload_multiple_text_files_router = APIRouter()

@upload_multiple_text_files_router.post("/upload-multiple-text-files")
async def upload_text_files(
    request: Request,
    collection_name: str = Form(...),
    files: List[UploadFile] = File(...),
    titles: List[str] = Form(...)
):
    
    # Initialization 
    mcol = await MongoDbCollectionController.init_class(request=request,)
    val = UploadFileValidation()


    await mcol.connect(collection_name=collection_name)
    # Validation - Collection name
    if val.check_collection_name(collection_name, request) == False:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=f"Collection name is not valid! Please provide the name of one of the following {request.app.mongo_collections_names}"
        )

    # Validate number of files matches number of titles
    if len(files) != len(titles):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content="Number of files must match number of titles!"
        )
    
    # Validate each file
    for file in files:
        if val.check_file_format(file, ".txt") == False:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=f"File format is not supported for {file.filename}!"
            )
        if val.check_file_size(file) == False:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=f"File size is too large for {file.filename}!"
            )
    
    # Processing - Create all documents
    documents = []
    file_info = []
    
    for file, title in zip(files, titles):
        txt = TextProcessing(file=file)
        document = txt.text_into_dict(
            collection_name=collection_name,
            title=title
        )
        documents.append(document)
        file_info.append({
            "title": title,
            "filename": file.filename,
            "file_id": document['file_id']
        })
    
    # Upload all documents to MongoDB using insert_many
    try:
        case,inseerted_ids = await mcol.insert_many(documents=documents)
        if case==False:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=f"Error inserting documents: check logging for more info"
            )
        else:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "message": "Text files uploaded successfully!",
                    "file_info": file_info,
                    "inserted_ids": [str(id) for id in inseerted_ids]
                }
            )
        
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=f"Error inserting documents: {e}"
        )