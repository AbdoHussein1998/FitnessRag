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
    MongoDB_COLLECTION_NAME_CHUNKED_IDS:str
    MongoDB_COLLECTION_NAME_EMBEDDED_CHUNKS:str


    QDRANT_DB_API_KEY:str
    QDRANT_DB_URL:str
    JSON_PROVIDER_DEFAULT_NAME:str
    LOCAL_EMBEDDING_MODEL:str
    VECTOR_SEARCH_FORMULA:str
    VECTOR_DATABASE_DEFULT_NAME:str



def get_basic_settings() -> BasicSettings:
    """
    Get the basic settings for the application.
    """
    return BasicSettings()

