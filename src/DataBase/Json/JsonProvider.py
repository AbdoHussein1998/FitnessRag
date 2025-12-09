from ProjectAssetes.BasicSetting import get_basic_settings
from DataBase.Json.Provider.MongoDb import MongoDbCollectionController,MongoChunksManager
class JsonProvider:
    def __init__(self, provider_name):
        self.basic_setting = get_basic_settings()
        if self.provider_name==None:
            self.provider_name=self.basic_setting.JSON_PROVIDER_DEFAULT_NAME
    
    def get_provider(self,):
        if self.provider_name==self.basic_setting.JSON_PROVIDER_DEFAULT_NAME:
            return MongoChunksManager,MongoDbCollectionController