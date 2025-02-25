import logging
from typing import List
from copy import deepcopy
from libnws.repository.base import BaseRepository
from libnws.model.nws_item import NWSItem
logger = logging.getLogger(__name__)


class InMemoryRepository(BaseRepository):
    def __init__(self):
        self._repository = []
    
    def _filter_mask(self, obj: NWSItem, filter: dict):
        mask = None
        for key, value in filter.items():
            mask_element = (getattr(obj, key) == value)
            if mask is None:
                mask = mask_element
            else:
                mask = mask & mask_element
        return mask
    
    def _get_index(self):
        if len(filter) == 1:
            key = list(filter.keys())[0]
            value = list(filter.values())[0]
            index = next((i for i, obj in enumerate(self._repository)
                          if getattr(obj, key) == value), None)
        else:
            index = next((i for i, obj in enumerate(self._repository)
                          if self._filter_mask(obj, filter)), None)
        return index

    def get_all(self) -> list:
        return self._repository

    def get(self, id_field: str, id_value: str) -> dict:
        if not isinstance(id_field, str):
            id_field = str(id_field)
        if not isinstance(id_value, str):
            id_value = str(id_value)
        return next((obj for obj in self._repository
                     if getattr(obj, id_field) == id_value), None)
    
    def filter_by(self, filter: dict) -> List[NWSItem]:
        if len(filter) == 1:
            key = list(filter.keys())[0]
            value = list(filter.values())[0]
            return [next((obj for obj in self._repository
                         if getattr(obj, key) == value), None)]
        else:
            items = []
            for key, value in filter.items():
                items.append(next((obj for obj in self._repository
                                  if getattr(obj, key) == value), None))
            return items
    
    def create(self, item: NWSItem) -> NWSItem:
        new_item = deepcopy(item)
        self._repository.append(new_item)
        return new_item

    def update(self, item: NWSItem, filter: dict) -> bool:
        index = self._get_index(filter)
        if index is not None:
            self._repository[index] = item
            return True
        return False
    
    def delete(self, item: NWSItem, filter: dict) -> bool:
        index = self._get_index(filter)
        if index is not None:
            self._repository.pop(index)
            return True
        return False
    
    def serialize(self, item):
        raise NotImplementedError
    
    def deserialize(self, data):
        raise NotImplementedError
