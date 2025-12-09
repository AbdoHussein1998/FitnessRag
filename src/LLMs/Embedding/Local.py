from sentence_transformers import SentenceTransformer
from ProjectAssetes.BasicSetting import get_basic_settings

class LocalEmbeddingProvider:
    def __init__(self,model_name):
        self.model = SentenceTransformer(model_name,trust_remote_code=True)

    @classmethod
    async def connect(cls,model_name):
       return cls(model_name)
    

    async def encode(self, sentences):
        vector=self.model.encode(sentences)
        return vector
    
    async def get_vector_dimensions(self):
        return self.model.get_sentence_embedding_dimension()
    