
from fastapi import Request
from fastapi.responses import JSONResponse

from ProjectAssetes import get_logger

class UploadFileValidation:
    def __init__(self):
        pass
    
    def check_file_format(self,file,format):
        if file.filename.endswith(format):
            return True
        return False
    
    def check_file_size(self,file):
        if file.size <= 2 * 1024 * 1024:
            return True
        return False
    

    def check_collection_name(self,collection_name,request:Request):
        if collection_name in request.app.mongo_collections_names:
            return True
        return False
    
