
from datetime import datetime
from dataclasses import dataclass
from libnws.model.nws_item import NWSItem


@dataclass(kw_only=True)
class ProductType(NWSItem):
    code: str
    name: str


@dataclass(kw_only=True)
class ProductLocation(NWSItem):
    code: str
    name: str


@dataclass(kw_only=True)
class Product(NWSItem):
    retrieved_at: datetime
    product_id: str
    wmo_id: str
    name: str
    code: str
    text: str
    issuing_office: str
    issued_at: datetime
