from abc import ABC,abstractmethod

class VectorDBInterface(ABC):

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def is_collection_existed(self) -> bool:
        pass

    @abstractmethod
    def list_all_collections(self) -> list:
        pass

    @abstractmethod
    def get_collection_info(self) -> dict:
        pass

    @abstractmethod
    def delete_collection(self):
        pass

    @abstractmethod
    def create_collection(self):
        pass

    @abstractmethod
    def insert_one(self):
        pass

    @abstractmethod
    def insert_many(self):
        pass

    @abstractmethod
    def search_by_vector(self):
        pass
    @abstractmethod
    def get_preproceesor(self):
        pass
    
    @abstractmethod
    def create_collection(self):
        pass
    def delete_collection(self):
        pass