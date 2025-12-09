
import uuid


class TextProcessing:
    def __init__(self, file):
        self.file = file

        
    def text_into_dict(self,collection_name,title)->dict:
        dic={}
        text = self.file.file.read().decode("utf-8")
        dic.update({"file_id":str(uuid.uuid4())})
        dic.update({"collection_name":collection_name})
        dic.update({"text":text})
        dic.update({"title":title})
        return dic
