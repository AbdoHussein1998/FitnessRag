#src\DataBase\VectorDB\VectorDBProviderFactory.py
from ProjectAssetes.BasicSetting import get_basic_settings
from DataBase.VectorDB.Providers.QdrantDb import QdrantDbProvider
from DataBase.VectorDB.Preprocessors import QdrantDBPreprocessor  
class VectorDbProviderFactory:
    def __init__(self,provider_name:str=None ):
        self.basic_setting = get_basic_settings()
        if provider_name==None:
            self.provider_name=self.basic_setting.VECTOR_DATABASE_DEFULT_NAME
        else:
            self.provider_name=provider_name

    def get_provider(self):
        if self.provider_name==self.basic_setting.VECTOR_DATABASE_DEFULT_NAME:
            return QdrantDBPreprocessor,QdrantDbProvider()



