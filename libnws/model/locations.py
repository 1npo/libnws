from dataclasses import dataclass
from libnws.model.nws_item import NWSItem


@dataclass(kw_only=True)
class Location(NWSItem):
    city: str
    state: str
    timezone: str
    grid_x: int
    grid_y: int
    forecast_office: str
    radar_station: str
    forecast_office_url: str
    forecast_extended_url: str
    forecast_hourly_url: str
    gridpoints_url: str
    observation_stations_url: str
