from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List
from libnws.model.nws_item import NWSItem


@dataclass(kw_only=True)
class Observation(NWSItem):
    retrieved_at: datetime
    station_or_zone_id: str
    observed_at: datetime
    icon_url: str
    text_description: str
    raw_message: str
    station_elevation_m: int
    station_elevation_mi: float
    temperature_c: float
    temperature_f: float
    dew_point_c: float
    dew_point_f: float
    wind_direction_deg_ang: int
    wind_direction_compass: str
    wind_speed_kmh: float
    wind_speed_mph: float
    wind_gust_kmh: float
    wind_gust_mph: float
    barometric_pressure_pa: int
    barometric_pressure_inhg: float
    sea_level_pressure_pa: int
    sea_level_pressure_inhg: float
    visibility_m: int
    visibility_mi: float
    max_temp_last_24h_c: float
    max_temp_last_24h_f: float
    min_temp_last_24h_c: float
    min_temp_last_24h_f: float
    precip_last_1h_mm: float
    precip_last_3h_mm: float
    precip_last_6h_mm: float
    relative_humidity_pc: float
    wind_chill_c: float
    wind_chill_f: float
    heat_index_c: float
    heat_index_f: float
    cloud_layers: Dict[str, str]


@dataclass(kw_only=True)
class ForecastPeriod(NWSItem):
    period_num: int
    period_name: str
    start_at: datetime
    end_at: datetime
    forecast_short: str
    forecast_detailed: str
    forecast_icon_url: str
    is_daytime: bool
    wind_speed: str
    wind_direction: str
    temperature_trend: str
    temperature_c: float
    temperature_f: float
    dew_point_c: float
    dew_point_f: float
    relative_humidity_pc: float
    precipitation_probability_pc: float


@dataclass(kw_only=True)
class Forecast(NWSItem):
    retrieved_at: datetime
    forecast_office: str
    grid_x: int
    grid_y: int
    generated_at: datetime
    updated_at: datetime
    periods: List[ForecastPeriod]
