#src\FastApi\Routes\AdminRoutes\ChunkDocument.py

from fastapi import APIRouter, status,Form,Depends,Request
from fastapi.responses import JSONResponse
from DataBase.Json.Provider.MongoDb import MongoDbCollectionController
from DataBase.DataBaseAssets import ConnectionsAssets
from DataBase.Json.Provider.MongoDb import ChunksManager
from FastApi.Schemas import ChunkDocumentRequest
from FastApi.Assistants import get_mongo_db_collections_names
from bson import ObjectId
from ProjectAssetes import get_logger

        
async def process_and_chunk_documents(docs: list,chunk_man_obj,col_chunks_obj,col_chunked_ids_obj,payload,logger) -> JSONResponse:
    """
    Process documents by chunking them and storing both chunks and metadata in MongoDB.
    
    Args:
        docs: List of document texts to be chunked
        chunk_man_obj: ChunksManager instance for text chunking operations
        col_chunks_obj: MongoDB collection controller for storing document chunks
        col_chunked_ids_obj: MongoDB collection controller for storing chunk ID metadata
        payload: Request payload containing collection_name and other metadata
        logger: Logger instance for tracking operations
    
    Returns:
        True Or Flase
    """
    try:
        # Initialize counter to track total number of chunks inserted across all documents
        total_inserted_ids = 0

        async for doc_chunks in chunk_man_obj.chunk_text(docs):
            # Insert all chunks from current document into the Chunks collection
            case,inserted_ids = await col_chunks_obj.insert_many(documents=doc_chunks)
            logger.info(f"we have {len(inserted_ids)} chunks")
            # Convert ObjectId instances to strings for JSON serialization
            inserted_ids_list = [str(id) for id in inserted_ids]
            # Build metadata document to track which chunks belong to which source file
            # Start with the list of chunk IDs that were just inserted
            inserted_ids_doc = {"inserted_ids": inserted_ids_list}
            inserted_ids_doc.update({"collection_name": payload.collection_name})
            inserted_ids_doc.update({"file_id": doc_chunks[0]["file_id"]})
            inserted_ids_doc.update({"mongo_id": doc_chunks[0]["mongo_id"]})
            inserted_ids_doc.update({"title": doc_chunks[0]["title"]})
            await col_chunked_ids_obj.insert_one(inserted_ids_doc)
            logger.info(f"we have inserted the inserted of ids {len(docs)} document, which is total ={len(inserted_ids)} ")
        
            # Accumulate total chunk count across all document batches
            total_inserted_ids += len(inserted_ids_list)
        
        # Return success response with processing statistics
        return JSONResponse(
            status_code=200,
            content={
                "message": "Text files uploaded successfully!",
                "number_of_files": len(docs),  # Total source documents processed
                "total_chunks": total_inserted_ids  # Total chunks created from all documents
            }
        )
    
    except Exception as e:
        # Re-raise exception to be handled by calling function
        logger.error(f"Error during document chunking: {str(e)}")
        raise


# API Route
chunk_document_router = APIRouter()
@chunk_document_router.post("/chunk_document")
async def chunk_document(payload:ChunkDocumentRequest,request:Request,
                         ):
    logger = get_logger(__name__)
    mongo_collections_names= request.app.mongo_collections_names
    #Valdiation
    payload_obj=payload
    if payload.collection_name is None:
        return JSONResponse(status_code=400, content={"message": "Collection name is required"})
    elif payload.collection_name not in mongo_collections_names:
        return JSONResponse(status_code=400, content={"message": "Collection name not found"})
    
    # initaliztion
    col_chunks_obj=await MongoDbCollectionController.init_class(request=request)
    col_chunked_ids_obj=await MongoDbCollectionController.init_class(request=request)
    chunk_man_obj= await ChunksManager.init_class()
    # Connecting
    await col_chunks_obj.connect(collection_name="Chunks")
    await col_chunked_ids_obj.connect(collection_name="Inserted_ids")

    
    docs=[]
            # Both if for finding one document and reutrn a list to work with process_and_chunk_documents
            # instead of addign isinstance to the function beacuse i'm bored :)

    # get document based on id
    if payload.document_id !=None :
        document=await col_chunks_obj.find_one(filter_dict={"_id":ObjectId(payload.document_id)})
        docs.append(document)
        if document is None:
            return JSONResponse(status_code=400, content={"message": "Document not found with this ID"})
        logger.info(f"we have {len(docs)} documents")
    # get document based on title
    elif payload.title :
        document=await col_chunks_obj.find_one(filter_dict={"title":payload.title})
        if document is None:
            return JSONResponse(status_code=400, content={"message": "Document not found with this Title"})
        docs.append(document)
        logger.info(f"we have {len(docs)} documents")
    
    
    # get all documents
    elif payload.document_id==None and payload.title ==None:
        #This to avoid loading all documents into the memory 
        async for batch in col_chunks_obj.stream_many_as_batches():
            if len(batch) == 0:
                logger.info("No documents found in the collection.")
                return JSONResponse(status_code=400, content={"message": "No documents found in the collection"})
                break
            else:
                result=await process_and_chunk_documents(
                    docs=batch,
                    chunk_man_obj=chunk_man_obj,
                    col_chunks_obj=col_chunks_obj,
                    col_chunked_ids_obj=col_chunked_ids_obj,
                    payload=payload,
                    logger=logger
                )
                return result

    
    # This is the case when there is one document
    result=await process_and_chunk_documents(
        docs=docs,
        chunk_man_obj=chunk_man_obj,
        col_chunks_obj=col_chunks_obj,
        col_chunked_ids_obj=col_chunked_ids_obj,
        payload=payload,
        logger=logger)
    if result is not None:
        return result
    else:
        return JSONResponse(status_code=400, content={"message": "No Documents"})



