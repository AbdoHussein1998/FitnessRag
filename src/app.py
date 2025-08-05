import uvicorn
import fastapi 
from FastApi.Routes import welcome_router



app = fastapi.FastAPI()
app.include_router(welcome_router)




if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
