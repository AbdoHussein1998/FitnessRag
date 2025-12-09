

from ProjectAssetes import get_basic_settings
from .Embedding.Local import LocalEmbeddingProvider

class EmbeddingProvider:
    def __init__(self, embedding_model: str = None):
        self.basic_setting = get_basic_settings()
        # If user provides a model, use it; else fallback to default
        self.embedding_model = embedding_model or self.basic_setting.LOCAL_EMBEDDING_MODEL

    def get_provider(self):
        # Return the actual model name and its provider
        return self.embedding_model, LocalEmbeddingProvider(self.embedding_model)

