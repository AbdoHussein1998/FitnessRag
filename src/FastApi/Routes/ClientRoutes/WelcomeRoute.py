from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
welcome_router = APIRouter()

@welcome_router.get("/welcome")
async def welcome():
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content="Welcome to Al-hakim Nutration and Workout!"
    )
    


