import csv
from typing import List, TextIO
from dataclasses import is_dataclass, fields
from libnws.repository.base import IRepository


class CSVRepository(IRepository):
    def __init__(
        self,
        file_path: str,
        columns: str,
        model,
        kwargs_csv: dict
    ):
        self._repository = []
        self.file_path = file_path
        self.columns = columns
        self.kwargs_csv = kwargs_csv
        self.model = model

    def _get_writer(self, buff: TextIO) -> csv.DictWriter:
        return csv.DictWriter(buff, fieldnames=self._get_columns(), **self.kwargs_csv)
    
    def _get_reader(self, buff: TextIO) -> csv.DictReader:
        return csv.DictReader(buff, fieldnames=self._get_columns(), **self.kwargs_csv)
    
    def _get_columns(self) -> List[str]:
        if self.columns is not None:
            return self.columns
        elif is_dataclass(self.model):
            return [field for field in fields(self.model)]
        else:
            return TypeError('Cannot determine CSV headers')

    def get_all(self) -> list:
        return self._repository

    def get_by_id(self, id: int) -> dict:
        pass
    
    def get_by_filter(self, filter: dict) -> list:
        pass
    
    def create(self, item: dict) -> dict:
        pass
    
    def update(self, item: dict) -> bool:
        pass
    
    def delete(self, id) -> bool:
        pass