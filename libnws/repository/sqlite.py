import os
import sqlite3
import glob
import logging
from dataclasses import asdict
from pathlib import Path
from libnws.repository.base import BaseRepository
from libnws.model.nws_item import NWSItem
logger = logging.getLogger(__name__)


SQLITE_SCHEMA_PATH = os.path.join(os.path.dirname(__file__), 'schemas/sqlite/')


class SQLiteRepository(BaseRepository):
    """
    :param sqlite_path: The path to the SQLite database to open (default: in-memory)
    :param sqlite_schema: The path to a file containing the schema to initialize
        a new database with
    """

    def __init__(
        self,
        sqlite_path: str = ':memory:',
        sqlite_schema_path: str = SQLITE_SCHEMA_PATH
    ):
        self.sqlite_path = sqlite_path
        self.sqlite_schema_path = sqlite_schema_path
        self.conn = sqlite3.connect(self.sqlite_path)
        self.curs = self.conn.cursor()

        if self.sqlite_path == ':memory:':
            self._init_new_sqlite_db()
        else:
            # The database will be empty (no tables) if it was just created. If the db
            # at sqlite_path is empty, initialize a new database using the
            # given sqlite_schema
            query = 'SELECT name FROM sqlite_master WHERE type="table"'
            if not self.curs.execute(query).fetchall():
                self._init_new_sqlite_db()

    def _init_new_sqlite_db(self):
        schema_files = glob.glob(os.path.join(self.sqlite_schema_path, '*.sql'))
        for schema_file in schema_files:
            with open(schema_file) as file:
                self.curs.executescript(file.read())
                logger.debug(f'Created "{Path(schema_file).stem}" tables')
        logger.info(f'Initialized new SQLite3 database at {self.sqlite_path}')
    
    def _res_to_item(self, res, nws_item: NWSItem) -> sqlite3.Cursor:
        res_cols = [desc[0] for desc in self.curs.description]
        records = []
        for row in res:
            record = {k:v for k,v in zip(res_cols, row)}
            records.append(nws_item(**record))
        return records

    def _get_filter_str(self, filter: dict) -> str:
        if len(filter) == 1:
            key = list(filter.keys())[0]
            value = list(filter.values())[0]
            if isinstance(value, str):
                value = f'"{value}"'
            filter_str = f'WHERE {key} == {value}'
        else:
            filter_str = ''
            for key, value in filter.items():
                if isinstance(value, str):
                    value = f'"{value}"'
                if not filter_str:
                    filter_str = f'WHERE {key} == {value}'
                else:
                    filter_str += f' AND {key} == {value}'
        return filter_str

    def get_all(self, table: str, nws_item: NWSItem) -> list:
        res = self.curs.execute(f'SELECT * FROM {table}').fetchall()
        return self._res_to_item(res, nws_item)

    def get(self, table: str, id_field: str, id_value: str, nws_item: NWSItem) -> list:
        query = f'SELECT * FROM {table} WHERE {id_field} == {id_value}'
        res = self.curs.execute(query).fetchall()
        return self._res_to_item(res, nws_item)
    
    def filter_by(self, table: str, nws_item: NWSItem, filter: dict) -> list:
        filter_str = self._get_filter_str(filter)
        res = self.curs.execute(f'SELECT * FROM {table} {filter_str}').fetchall()
        return self._res_to_item(res, nws_item)
    
    def create(self, table: str, item: NWSItem) -> int:
        record = self.serialize(item)
        fields = ', '.join([k for k in record.keys()])
        named_params = ', '.join([f':{k}' for k in record.keys()])
        query = f'INSERT OR IGNORE INTO {table} ({fields}) VALUES ({named_params})'
        self.curs.execute(query, record)
        self.conn.commit()
        return self.curs.lastrowid

    def update(self, table: str, item: NWSItem, filter: dict) -> bool:
        record = self.serialize(item)
        update_str = ', '.join([f'{k} = :{k}' for k in record.keys() if k != 'id'])
        filter_str = self._get_filter_str(filter)
        query = f'UPDATE OR IGNORE {table} SET {update_str} {filter_str}'
        self.curs.execute(query, record)
        self.conn.commit()
        if self.curs.rowcount >= 1:
            return True
        else:
            return False

    def delete(self, table: str, filter: dict) -> bool:
        filter_str = self._get_filter_str(filter)
        print(filter_str)
        self.curs.execute(f'DELETE FROM {table} {filter_str}', )
        self.conn.commit()
        if self.curs.rowcount >= 1:
            return True
        else:
            return False
    
    def serialize(self, nws_item: NWSItem) -> dict:
        return asdict(nws_item)

    def deserialize(self, data, nws_item: NWSItem) -> NWSItem:
        return nws_item(**data)
