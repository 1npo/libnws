from abc import ABC, abstractmethod
from libnws.model.nws_item import NWSItem


class BaseRepository(ABC):
    @abstractmethod
    def get_all(self):
        raise NotImplementedError

    @abstractmethod
    def get(self, id: int):
        raise NotImplementedError
    
    @abstractmethod
    def filter_by(self, filter: dict):
        raise NotImplementedError

    @abstractmethod
    def create(self, item: NWSItem) -> NWSItem:
        raise NotImplementedError

    @abstractmethod
    def update(self, item: NWSItem) -> bool:
        raise NotImplementedError

    @abstractmethod
    def delete(self, item: NWSItem) -> bool:
        raise NotImplementedError
    
    @abstractmethod
    def serialize(self, item: NWSItem) -> dict:
        raise NotImplementedError
    
    @abstractmethod
    def deserialize(self, data: dict) -> NWSItem:
        raise NotImplementedError
