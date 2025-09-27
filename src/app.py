#src/app.py

from ProjectAssetes import load_dotenv
import uvicorn
import fastapi 
from FastApi import fastapi_lifespan
from FastApi.Routes import welcome_router,upload_text_file_router,create_collection_in_mongo_router
from FastApi.Routes import delete_collection_in_mongo_router
load_dotenv()  # Load environment variables



app = fastapi.FastAPI(lifespan=fastapi_lifespan)
app.include_router(welcome_router)
app.include_router(upload_text_file_router)
app.include_router(create_collection_in_mongo_router)
app.include_router(delete_collection_in_mongo_router)






if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)




