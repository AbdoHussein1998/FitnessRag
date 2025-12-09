


from DataBase.TEXT import TextProcessing
from fastapi import APIRouter, status,Form,Request
from fastapi.responses import JSONResponse
from LLMs.EmbeddingProvider import EmbeddingProvider
from DataBase.VectorDB.VectorDBProviderFactory import VectorDbProviderFactory
from FastApi.Schemas import CreateVectorCollectionRequestPayload

create_vector_collection_router = APIRouter()
@create_vector_collection_router.post("/create_vector_collection")
async def create_vector_collection(request:Request,payload:CreateVectorCollectionRequestPayload):

    # Intializtion
    embedding_model_name, embedding_model = EmbeddingProvider(embedding_model=payload.embedding_model).get_provider() 
    print("Using embedding model:", embedding_model_name)
   
    vector_preprocessor,col_vector_controller= VectorDbProviderFactory(provider_name=payload.vector_db_name).get_provider()
    # 
    embedding_model.connect(payload.embedding_model)
    case = await col_vector_controller.connect(collection_name=payload.collection_name)
    if case is True:
        return JSONResponse(status_code=400, content={"message": "the collection is already exist"}) 
    
    # Create new collection
    case=await col_vector_controller.create_collection(
        collection_name=payload.collection_name,
        vector_dimension=await embedding_model.get_vector_dimensions(),
        distance=payload.distance
    )
    if case is False:
        return JSONResponse(status_code=400, content={"message": "collection creation failed"})
    
    else:
        return JSONResponse(
            status_code=200,
            content={"message": "collection created successfully"}
        )
  



