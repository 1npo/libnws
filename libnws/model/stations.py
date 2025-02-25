from dataclasses import dataclass
from datetime import datetime
from libnws.model.nws_item import NWSItem


@dataclass(kw_only=True)
class Station(NWSItem):
    retrieved_at: datetime
    station_id: str
    name: str
    timezone: str
    lat: float
    lon: float
    elevation_m: float
    elevation_mi: float
    forecast_url: str
    county_url: str
    fire_weather_zone_url: str
