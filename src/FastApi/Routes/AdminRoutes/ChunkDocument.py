#src\FastApi\Routes\AdminRoutes\ChunkDocument.py

from fastapi import APIRouter, status,Form,Depends,Request
from fastapi.responses import JSONResponse
from DataBase.Json.Provider.MongoDb import MongoDbCollection
from DataBase.DataBaseAssets import ConnectionsAssets
from DataBase.Json.Provider.MongoDb import ChunksManager
from FastApi.Schemas import ChunkDocumentRequest
from FastApi.Assistants import get_mongo_db_collections_names
from bson import ObjectId
from ProjectAssetes import get_logger
from pprint import pprint as pp



chunk_document_router = APIRouter()

@chunk_document_router.post("/chunk_document")
async def chunk_document(payload:ChunkDocumentRequest,request:Request,
                         ):
    
    logger = get_logger(__name__)

    mongo_collections_names= request.app.mongo_collections_names
 
    # #Valdiation
    payload_obj=payload
    if payload.collection_name is None:
        return JSONResponse(status_code=400, content={"message": "Collection name is required"})
    elif payload.collection_name not in mongo_collections_names:
        return JSONResponse(status_code=400, content={"message": "Collection name not found"})
    
    # initaliztion
    col_doc_obj=await MongoDbCollection.init_class(request=request,collection_name=payload.collection_name)
    col_chunked_ids_obj=await MongoDbCollection.init_class(request=request, collection_name="inserted_ids")
    col_chunks_obj=await MongoDbCollection.init_class(request=request, collection_name="chunks")

    chunk_obj= await ChunksManager.init_class()
    docs=[]
    
    # get document based on id
    if payload.document_id !=None :
        document=await col_doc_obj.find_one(filter_dict={"_id":ObjectId(payload.document_id)})
        document
        if document is None:
            return JSONResponse(status_code=400, content={"message": "Document not found with this ID"})
        docs.append(document["text"])
        logger.info(f"we have {len(docs)} documents")
    # get document based on title
    elif payload.title :
        document=await col_doc_obj.find_one(filter_dict={"title":payload.title})
        if document is None:
            return JSONResponse(status_code=400, content={"message": "Document not found with this Title"})
        docs.append(document["text"])
        logger.info(f"we have {len(docs)} documents")
    # get all documents
    elif payload.document_id==None and payload.title ==None:
        documents=await col_doc_obj.find_many()
        docs.extend(documents)
        logger.info(f"we have {len(docs)} documents")

        if len(docs)==0:
            return JSONResponse(status_code=400, content={"message": "No documents found in this collection"})
        
    try:
        #chunking and inserting 
        total_inserted_ids=0

        async for doc_chunks in chunk_obj.chunk_text(docs):

            inserted_ids = await col_chunks_obj.insert_many(documents=doc_chunks)
            logger.info(f"we have {len(inserted_ids)} chunks")

            inserted_ids_list=[str(id) for id in inserted_ids]
            inserted_ids_doc={"inserted_ids":inserted_ids_list}
            inserted_ids_doc.update({"collection_name":payload.collection_name})
            inserted_ids_doc.update({"file_id":doc_chunks[0]["file_id"]})
            inserted_ids_doc.update({"mongo_id":doc_chunks[0]["mongo_id"]})
            inserted_ids_doc.update({"title":doc_chunks[0]["title"]})
            await col_chunked_ids_obj.insert_one(inserted_ids_doc)

            logger.info(f"we have inserted the inserted of ids {len(docs)} document, which is total ={len(inserted_ids)} ")
            total_inserted_ids+=len(inserted_ids_list)
        return JSONResponse(
            status_code=200,
            content={
                "message": "Text files uploaded successfully!",
                "number_of_files": len(docs),
                "total_chunks": total_inserted_ids
            }
        )

    except Exception as e:
        logger.error(f"Error inserting documents: {e}")
        return JSONResponse(status_code=400, content={"message": "Error inserting documents"})


        
       