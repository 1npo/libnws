
import logging
from typing import Tuple
from requests_cache import CachedSession
from libnws.render.decorators import display_spinner
from libnws.api.api_request import api_request
from libnws.api import USCB_API_GEOCODE, NWS_API_POINTS
from libnws.model.locations import Location
logger = logging.getLogger(__name__)


# See: https://geocoding.geo.census.gov/geocoder/Geocoding_Services_API.html
def uscb_geocode(
	session: CachedSession,
	address: str
) -> Tuple[float, float] | None:
	"""Get the lat and lon for a street address using the US Census Bureau's free
	geocoding API"""

	coord_data = api_request(session, USCB_API_GEOCODE + address.replace(' ', '+'))
	response = coord_data.get('response')
	try:
		coords = response['result']['addressMatches'][0]['coordinates']
		lat = round(coords['y'], 2)
		lon = round(coords['x'], 2)
		logger.debug(f'Geocoded address {address} to {lat}, {lon}')
		return (lat, lon)
	except KeyError:
		return None


@display_spinner('Getting location data...')
def get_location(
	session: CachedSession,
	address: str
) -> Location:
	coords = uscb_geocode(session, address)
	coords_str = f'{coords[0]},{coords[1]}'
	location_data = api_request(session, NWS_API_POINTS + coords_str)
	response = location_data.get('response')
	location_dict = {
		'city':                     (response.get('properties', {})
							   				 .get('relativeLocation', {})
											 .get('properties', {})
											 .get('city')),
		'state':                    (response.get('properties', {})
							   				 .get('relativeLocation', {})
											 .get('properties', {})
											 .get('state')),
		'timezone':                 response.get('properties', {}).get('timeZone'),
		'grid_x':                   response.get('properties', {}).get('gridX'),
		'grid_y':                   response.get('properties', {}).get('gridY'),
		'forecast_office':      	response.get('properties', {}).get('cwa'),
		'radar_station':            response.get('properties', {}).get('radarStation'),
		'forecast_office_url':      response.get('properties', {}).get('forecastOffice'),
		'forecast_extended_url':    response.get('properties', {}).get('forecast'),			# /gridpoints/{wfo}/{x},{y}/forecast
		'forecast_hourly_url':      response.get('properties', {}).get('forecastHourly'),	# /gridpoints/{wfo}/{x},{y}/forecast/hourly
		'gridpoints_url':           (response.get('properties', {})
							   				 .get('forecastGridData')),						# /gridpoints/{wfo}/{x},{y}
		'observation_stations_url': (response.get('properties', {})
							   				 .get('observationStations')),					# /gridpoints/{wfo}/{x},{y}/stations
	}
	return Location(**location_dict)
