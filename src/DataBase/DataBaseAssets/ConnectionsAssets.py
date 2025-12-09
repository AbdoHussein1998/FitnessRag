
from fastapi import Request
from ProjectAssetes import get_basic_settings
class ConnectionsAssets:
    def __init__(self,request:Request,):
        self.request=request
        self.mongo_db=self.request.app.mongo_db
        self.basic_settings=get_basic_settings()

        
        
        
        