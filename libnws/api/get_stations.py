from typing import List
from datetime import datetime
from requests_cache import CachedSession
from libnws.render.decorators import display_spinner
from libnws.api.get_weather import process_measurement_values
from libnws.api.conversions import convert_measures
from libnws.api.api_request import api_request
from libnws.api import NWS_API_STATIONS, NWS_API_GRIDPOINTS
from libnws.model.stations import Station


def process_station_data(feature: dict, retrieved_at: datetime) -> Station:
	"""Format the station data returned from /gridpoints or /stations"""
	station_coords = feature.get('geometry').get('coordinates')
	if station_coords and isinstance(station_coords, list):
		station_lat = station_coords[0]
		station_lon = station_coords[1]
	else:
		station_lat = None
		station_lon = None
	station = {
		'retrieved_at':				retrieved_at,
		'station_id':      			(feature.get('properties', {})
											.get('stationIdentifier')),
		'name':    					feature.get('properties', {}).get('name'),
		'lat':     					station_lat,
		'lon':     					station_lon,
		'timezone':					feature.get('properties', {}).get('timeZone'),
		'forecast_url':				feature.get('properties', {}).get('forecast'),
		'county_url':				feature.get('properties', {}).get('county'),
		'fire_weather_zone_url':	feature.get('properties', {}).get('fireWeatherZone'),
	}
	elevation_measure = feature.get('properties', {})
	station.update(process_measurement_values(elevation_measure,
											  {'elevation': 'elevation'},
											  {'elevation': 'wmoUnit:m'}))
	station = convert_measures(station)
	return Station(**station)


@display_spinner('Getting station...')
def get_station(session: CachedSession, station_id: dict) -> Station:
	station_data = api_request(session, NWS_API_STATIONS + station_id)
	response = station_data.get('response')
	retrieved_at = station_data.get('retrieved_at')
	return process_station_data(response, retrieved_at)


def get_stations(session: CachedSession, url: str) -> List[Station]:
	stations_data = api_request(session, url)
	response = stations_data.get('response')
	retrieved_at = stations_data.get('retrieved_at')
	stations = []
	for feature in response.get('features', {}):
		stations.append(process_station_data(feature, retrieved_at))
	return stations


@display_spinner('Getting stations usable in grid area...')
def get_stations_by_grid(
	session: CachedSession,
	forecast_office: str,
	gridpoints: dict
) -> List[Station]:
	return get_stations(session, (NWS_API_GRIDPOINTS 
								  + f'/{forecast_office}/{gridpoints}/stations'))


@display_spinner('Getting local stations...')
def get_stations_near_location(session: CachedSession, location: dict) -> List[Station]:
	return get_stations(session, location.observation_stations_url)
