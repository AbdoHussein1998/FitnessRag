from abc import ABC, abstractmethod



class CollectionControllerInterface(ABC):

    @abstractmethod
    def connect():
        pass
    @abstractmethod
    def disconnect():
        pass
    @abstractmethod
    def is_collection_existed():
        pass
    @abstractmethod
    def list_collections():
        pass
    @abstractmethod
    def init_class():
        pass
    @abstractmethod
    def insert_one():
        pass
    @abstractmethod
    def insert_many():
        pass
    @abstractmethod
    def find_one():
        pass
    @abstractmethod
    def find_many():
        pass
    @abstractmethod
    def stream_many_as_batches():
        pass
    @abstractmethod
    def create_collection():
        pass
    @abstractmethod
    def delete_collection():
        pass    