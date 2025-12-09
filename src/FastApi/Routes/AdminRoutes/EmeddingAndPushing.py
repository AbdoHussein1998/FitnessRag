


from FastApi.Assistants import UploadFileValidation
from DataBase.TEXT import TextProcessing
from fastapi import APIRouter, status,UploadFile,File,Form,Request
from fastapi.responses import JSONResponse
from DataBase.Json.Provider.MongoDb import MongoDbCollectionController
from FastApi.Schemas import EmbeddDocumentRequestPayload
from LLMs.EmbeddingProvider import EmbeddingProvider
from DataBase.VectorDB.VectorDBProviderFactory import VectorDbProviderFactory

embedding_and_pushing_router = APIRouter()
@embedding_and_pushing_router.post("/embedding-and-pushing")
async def upload_text_file(request:Request,payload: EmbeddDocumentRequestPayload ,):

    col_mongo_chunks=await MongoDbCollectionController.init_class(request=request)
    vector_preprocessor,col_vector_controller= VectorDbProviderFactory(provider_name=payload.vector_db_name).get_provider()
    embedding_model_name,embedding_model= EmbeddingProvider(embedding_model=payload.embedding_model).get_local_embedding_provider()

    await col_mongo_chunks.connect(collection_name=payload.chunks_text_collection_name)
    

    case=await col_vector_controller.connect(collection_name=payload.vector_collection_name)
    if case is False:
        return JSONResponse(status_code=400, content={"message": "Vector DB connection failed"})
    
    



    async for batche in col_mongo_chunks.stream_many_as_batches():
            for document in batche:
               vector=embedding_model.encode(document["text"])
    


               
        