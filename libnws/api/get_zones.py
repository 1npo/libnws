import json
from typing import List
from datetime import datetime
from requests_cache import CachedSession
from libnws.render.decorators import display_spinner
from libnws.api.api_request import api_request, parse_timestamp
from libnws.api.get_stations import process_station_data
from libnws.api.get_weather import process_observations_data
from libnws.api import (
    NWS_API_ZONES,
    NWS_API_ZONE_FORECASTS,
    VALID_NWS_ZONES,
)
from libnws.model.zones import Zone, ZoneForecast, ZoneForecastPeriod
from libnws.model.stations import Station
from libnws.model.weather import Observation


def process_zone_data(zone_data: list, retrieved_at: datetime) -> Zone:
    geometry = zone_data.get('geometry', {})
    geometry_json = None
    if geometry:
        geometry_json = json.dumps({'coordinates': geometry.get('coordinates')})
    zone_dict = {
        'retrieved_at':         retrieved_at,
        'zone_id':              zone_data.get('properties', {}).get('id'),
        'grid_id':              zone_data.get('properties', {}).get('gridIdentifier'),
        'awips_id':             (zone_data.get('properties', {})
                                          .get('awipsLocationIdentifier')),
        'name':                 zone_data.get('properties', {}).get('name'),
        'zone_type':            zone_data.get('properties', {}).get('type'),
        'state':                zone_data.get('properties', {}).get('state'),
        'url':                  zone_data.get('properties', {}).get('@id'),
        'timezones':            zone_data.get('properties', {}).get('timeZone'),
        'county_warning_areas': zone_data.get('properties', {}).get('cwa'),
        'effective_at':         (parse_timestamp(zone_data.get('properties', {})
                                                          .get('effectiveDate'))),
        'expires_at':           (parse_timestamp(zone_data.get('properties', {})
                                                          .get('expirationDate'))),
        'forecast_offices':     zone_data.get('properties', {}).get('forecastOffices'),
        'observation_stations': (zone_data.get('properties', {})
                                          .get('observationStations')),
        'multi_polygon':        geometry_json,
    }
    return Zone(**zone_dict)


@display_spinner('Getting zone...')
def get_zone(
    session: CachedSession,
    zone_type: str,
    zone_id: str
) -> Zone:
    if zone_type not in VALID_NWS_ZONES:
        raise ValueError((
            f'Invalid zone type provided: {zone_type}. '
            f'Valid zones are: {", ".join(VALID_NWS_ZONES)}'))
    zone_data = api_request(session, NWS_API_ZONES + f'/{zone_type}/{zone_id}')
    response = zone_data.get('response')
    retrieved_at = zone_data.get('retrieved_at')
    return process_zone_data(response, retrieved_at)


@display_spinner('Getting all zones...')
def get_zones(
    session: CachedSession,
    zone_type: str = None
) -> List[Zone]:
    if zone_type:
        zones_data = api_request(session, NWS_API_ZONES + f'/{zone_type}')
    else:
        zones_data = api_request(session, NWS_API_ZONES)
    response = zones_data.get('response')
    retrieved_at = zones_data.get('retrieved_at')
    zones = []
    for feature in response.get('features', {}):
        zones.append(process_zone_data(feature, retrieved_at))
    return zones


@display_spinner('Getting stations servicing zone...')
def get_zone_stations(
    session: CachedSession,
    zone_id: str
) -> List[Station]:
    zone_stations_data = api_request(session, (NWS_API_ZONE_FORECASTS
                                               + f'{zone_id}/stations'))
    response = zone_stations_data.get('response')
    retrieved_at = zone_stations_data.get('retrieved_at')
    zone_stations = []
    for feature in response.get('features', {}):
        zone_stations.append(process_station_data(feature, retrieved_at))
    return zone_stations


@display_spinner('Getting observations for zone...')
def get_zone_observations(
    session: CachedSession,
    zone_id: str
) -> List[Observation]:
    zone_observations_data = api_request(session, (NWS_API_ZONE_FORECASTS
                                                   + f'{zone_id}/observations'))
    response = zone_observations_data.get('response')
    retrieved_at = zone_observations_data.get('retrieved_at')
    zone_observations = []
    for feature in response.get('features', {}):
        zone_observations.append(process_observations_data(feature,
                                                           retrieved_at,
                                                           zone_id))
    return zone_observations


@display_spinner('Getting forecast for zone...')
def get_zone_forecast(
    session: CachedSession,
    zone_id: str
) -> ZoneForecast:
    zone_forecast_data = api_request(session,
                                     NWS_API_ZONE_FORECASTS + f'{zone_id}/forecast')
    response = zone_forecast_data.get('response')
    retrieved_at = zone_forecast_data.get('retrieved_at')
    forecast_dict = {
        'retrieved_at':     retrieved_at,
        'zone_id':          zone_id,
        'forecasted_at':    (parse_timestamp(response.get('properties', {})
                                                     .get('updated'))),
        'periods':          []
    }
    forecast = ZoneForecast(**forecast_dict)
    for period in response.get('properties', {}).get('periods', {}):
        if period and isinstance(period, dict):
            period_dict = {
                'period_num':        period.get('number'),
                'period_name':       period.get('name'),
                'forecast_detailed': period.get('detailedForecast'),
            }
            forecast_period = ZoneForecastPeriod(**period_dict)
            forecast.periods.append(forecast_period)
    return forecast
