# src/ProjectAssetes/AssetesFunctions.py
import sys
import os
import logging
import dotenv 
from fastapi import Request
from motor.motor_asyncio import AsyncIOMotorCollection
def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    
    # Only add handler if logger doesn't have any handlers yet
    if not logger.handlers:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        
        logger.addHandler(console_handler)
    
    return logger

def load_dotenv():
    """
    Load environment variables from a .env file.
    """
    logger = get_logger(__name__)
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        dotenv.load_dotenv(dotenv_path)
        logger.info(f"Loaded environment variables from {dotenv_path}")
    else:
        logger.error(f"Loaded environment variables from {dotenv_path}")
        raise FileNotFoundError(f".env file not found at {dotenv_path}")
    




