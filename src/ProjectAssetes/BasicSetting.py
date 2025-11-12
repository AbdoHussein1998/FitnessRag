# src/ProjectAssetes/BasicSetting.py

from pydantic_settings import BaseSettings




class BasicSettings(BaseSettings):   
    """
    Basic settings for the application.
    """
    APP_NAME:str
    APP_VERSION:str
    MongoDB_URL:str
    MongoDB_DB_NAME:str
    MongoDB_COLLECTION_NAME_DR_MIKE:str
    MongoDB_COLLECTION_NAME_JEFF_NIPPARD:str
    MongoDB_COLLECTION_NAME_TOMAS_DELURE:str

    MongoDB_COLLECTION_NAME_CHUNKS:str
    MongoDB_COLLECTION_NAME_INSERTED_IDS:str


    QDRANT_DB_API_KEY:str
    QDRANT_DB_URL:str
    

def get_basic_settings() -> BasicSettings:
    """
    Get the basic settings for the application.
    """
    return BasicSettings()

