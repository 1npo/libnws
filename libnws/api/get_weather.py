"""
"""

import logging
from typing import List
from datetime import datetime
from requests_cache import CachedSession
from libnws.render.decorators import display_spinner
from libnws.main import BUG_REPORT_MESSAGE
from libnws.api.api_request import api_request, parse_timestamp
from libnws.api.conversions import convert_measures
from libnws.api import (
	NWS_API_STATIONS,
	METAR_CLOUD_COVER_MAP,
	WMI_UNIT_MAP,
)
from libnws.model.weather import Observation, Forecast, ForecastPeriod
from libnws.model.locations import Location
logger = logging.getLogger(__name__)


def process_measurement_values(
	data: dict,
	field_map: dict,
	expected_units: dict
) -> dict:
	"""Flatten measurement values in API responses
	
	The NWS API returns measurements as a dictionary of two items, where one item
	is a string that describes the unit of measure, and the other is the actual
	measurement value.

	This function standardizes the field name, adds the unit of measure as a suffix
	to the field name, and returns a dictionary where the key is this new field name
	and the value is the measurement.
	
	For example, this dictionary:
	
	.. code-block:: python

		{
			'temperature': {
				'unitCode': 'wmoUnit:degC',
				'value': 31.2,
			},
			"windSpeed": {
				"unitCode": "wmoUnit:km_h-1",
				"value": 3.564,
			}
		}

	Will be flattened into this dictionary:

	.. code-block:: python

		{
			'temperature_c': 31.2,
			'wind_speed_kmh': 3.564,
		}

	The WMI_UNIT_MAP global in `nwsc.api.__init__` maps all the WMO unit strings to
	appreviated field suffixes.
	
	:param data: A dictionary containing a set of measurements.
	:param field_map: A mapping of API response field names to standardized `nwsc`
		field names.
	:param expected_units: The units of measure that are expected from the API for each
		measurement in `data`. Must contain the same number of items as `field_map` and
		have the same keys.
	:returns: Any items in `data` that are present in `field_map`, reformatted as a flat
		dictionary where all values are measurements instead of dicts.
	"""

	if set(field_map.keys()) != set(expected_units.keys()):
		raise ValueError((
			'The given field_map and expected_units don\'t contain the same keys. '
			f'{field_map.keys()=}, {expected_units.keys()=}. {BUG_REPORT_MESSAGE}'
		))
	
	new_data = {}
	for old_name, new_name in field_map.items():
		value = data.get(old_name, {}).get('value')
		expected_unit = expected_units.get(old_name)
		actual_unit = data.get(old_name, {}).get('unitCode')
		if actual_unit:
			if actual_unit != expected_unit:
				logger.debug((
					f'An actual value and unit are present for {old_name}, but the '
					f'measurement unit is unexpected ({expected_unit=}, {actual_unit=}). '
					'Using actual unit.'))
			if actual_unit not in WMI_UNIT_MAP:
				logger.debug((
					f'No standard field suffix for measurement unit ({actual_unit}). '
					f'Using the expected unit field suffix instead. '
					BUG_REPORT_MESSAGE))
				unit_suffix = WMI_UNIT_MAP.get(expected_unit)
			else:
				unit_suffix = WMI_UNIT_MAP.get(actual_unit)
		else:
			unit_suffix = WMI_UNIT_MAP.get(expected_unit)
		new_data.update({f'{new_name}_{unit_suffix}': value})
	return new_data


def process_cloud_layers(cloud_layers_data: list) -> dict:
	"""Flatten cloud layers and convert cloud cover codes to English descriptions

	The NWS API returns a list dictionaries to describe cloud layers. Each dictionary
	contains a measurement that indicates the height of the cloud layer, and a code that
	describes the cloud cover at that layer.

	This function processes this list and returns a dictionary where the keys are strings
	that represent the cloud layer height, and the values are an English description
	of the cloud cover for that layer.

	For example, this list of dictionaries:

	.. code-block:: python

		"cloudLayers": [
		{
			"base": {
			"unitCode": "wmoUnit:m",
			"value": 370
			},
			"amount": "FEW"
		},
		{
			"base": {
			"unitCode": "wmoUnit:m",
			"value": 640
			},
			"amount": "SCT"
		},
		}

	Will be flattened into this dictionary:

	.. code-block:: python

		{
			'370m': 'Few Clouds',
			'640m': 'Scattered Clouds',
		}

	The METAR_CLOUD_COVER_MAP global in `nwsc.api.__init__` maps all the cloud cover
	codes to English descriptions.
	"""

	cloud_layers = {}
	for layer in cloud_layers_data:
		if layer and isinstance(layer, dict):
			cloud_layer_height_unit = layer.get('base', {}).get('unitCode')
			cloud_layer_height_unit = WMI_UNIT_MAP.get(cloud_layer_height_unit)
			cloud_layer_height = layer.get('base', {}).get('value')
			cloud_layer = f'{cloud_layer_height}{cloud_layer_height_unit}'
			cloud_cover_at_layer = layer.get('amount')
			cloud_cover_at_layer = METAR_CLOUD_COVER_MAP.get(cloud_cover_at_layer)
			cloud_layers.update({cloud_layer: cloud_cover_at_layer})
	return cloud_layers


def process_observations_data(
	observations_data: list,
	retrieved_at: datetime,
	station_or_zone_id: str
) -> Observation:
	observations = {
		'retrieved_at':	retrieved_at,
		'station_or_zone_id':	station_or_zone_id,
		'observed_at':      	(parse_timestamp(observations_data
													.get('properties', {})
													.get('timestamp'))),
		'icon_url':         	observations_data.get('properties', {}).get('icon'),
		'text_description': 	(observations_data.get('properties', {})
												  .get('textDescription')),
		'raw_message':			observations_data.get('properties', {}).get('rawMessage'),
	}
	observation_field_map = {
		'elevation':                    'station_elevation',
		'temperature':                  'temperature',
		'dewpoint':                     'dew_point',
		'windDirection':                'wind_direction',    
		'windSpeed':                    'wind_speed',
		'windGust':                     'wind_gust',
		'barometricPressure':           'barometric_pressure',
		'seaLevelPressure':             'sea_level_pressure',
		'visibility':                   'visibility',
		'maxTemperatureLast24Hours':    'max_temp_last_24h',
		'minTemperatureLast24Hours':    'min_temp_last_24h',
		'precipitationLastHour':        'precip_last_1h',
		'precipitationLast3Hours':      'precip_last_3h',
		'precipitationLast6Hours':      'precip_last_6h',
		'relativeHumidity':             'relative_humidity',
		'windChill':                    'wind_chill',
		'heatIndex':                    'heat_index',
	}
	expected_units = {
		'elevation':                    'wmoUnit:m',
		'temperature':                  'wmoUnit:degC',
		'dewpoint':                     'wmoUnit:degC',
		'windDirection':                'wmoUnit:degree_(angle)',    
		'windSpeed':                    'wmoUnit:km_h-1',
		'windGust':                     'wmoUnit:km_h-1',
		'barometricPressure':           'wmoUnit:Pa',
		'seaLevelPressure':             'wmoUnit:Pa',
		'visibility':                   'wmoUnit:m',
		'maxTemperatureLast24Hours':    'wmoUnit:degC',
		'minTemperatureLast24Hours':    'wmoUnit:degC',
		'precipitationLastHour':        'wmoUnit:mm',
		'precipitationLast3Hours':      'wmoUnit:mm',
		'precipitationLast6Hours':      'wmoUnit:mm',
		'relativeHumidity':             'wmoUnit:percent',
		'windChill':                    'wmoUnit:degC',
		'heatIndex':                    'wmoUnit:degC',
	}
	observation_measurements = observations_data.get('properties', {})
	observations.update(process_measurement_values(observation_measurements,
												   observation_field_map,
												   expected_units))
	cloud_layer_data = observations_data.get('properties', {}).get('cloudLayers')
	cloud_layers = process_cloud_layers(cloud_layer_data)
	observations.update({'cloud_layers': cloud_layers})
	observations = convert_measures(observations)
	return Observation(**observations)


def process_forecast_data(
	forecast_data: list,
	retrieved_at: datetime,
	location: Location
) -> Forecast:
	len_periods = len(forecast_data.get('properties', {}).get('periods'))
	forecast_dict = {
		'retrieved_at':	retrieved_at,
		'forecast_office':		location.forecast_office,
		'grid_x':				location.grid_x,
		'grid_y':				location.grid_y,
		'generated_at':			(parse_timestamp(forecast_data.get('properties', {})
															  .get('generatedAt'))),
		'updated_at':			(parse_timestamp(forecast_data.get('properties', {})
															  .get('updateTime'))),
		'periods':				[],
	}
	forecast = Forecast(**forecast_dict)
	for i in range(0, len_periods):
		period = forecast_data.get('properties', {}).get('periods', {})
		if period and isinstance(period, list):
			period = period[i]
			# The temperature unit and value in a forecast response aren't combined in a
			# dict with 'unitCode' and 'value' keys like all other measures. They're flat
			# fields ('temperatureUnit' and 'temperature'), so I don't include them in the
			# process_measurement_values() call.
			#
			# TODO: Find a better and more uniform way to process all measurements.
			temp_unit = WMI_UNIT_MAP.get(period.get('temperatureUnit'))
			forecast_period_dict = {
				'period_num':				period.get('number'), 
				'period_name':              period.get('name'),
				'forecast_short':        	period.get('shortForecast'),
				'forecast_detailed':     	period.get('detailedForecast'),
				'forecast_icon_url':     	period.get('icon'),
				'is_daytime':               period.get('isDaytime'),
				'wind_speed':               period.get('windSpeed'),
				'wind_direction':           period.get('windDirection'),
				'temperature_trend':        period.get('temperatureTrend'),
				f'temperature_{temp_unit}':	period.get('temperature'),
				'start_at':          		parse_timestamp(period.get('startTime')),
				'end_at':            		parse_timestamp(period.get('endTime')),
			}
			field_map = {
				'dewpoint':						'dew_point',
				'relativeHumidity':				'relative_humidity',
				'probabilityOfPrecipitation':	'precipitation_probability',
			}
			expected_types = {
				'dewpoint':						'wmoUnit:degC',
				'relativeHumidity':				'wmoUnit:percent',
				'probabilityOfPrecipitation':	'wmoUnit:percent',
			}
			forecast_period_dict.update(process_measurement_values(period,
																   field_map,
																   expected_types))
			forecast_period_dict = convert_measures(forecast_period_dict)
			forecast_period = ForecastPeriod(**forecast_period_dict)
			forecast.periods.append(forecast_period)
	return forecast


@display_spinner('Getting all station observations...')
def get_all_observations(
	session: CachedSession,
	station_id: str
) -> List[Observation]:
	observations_data = api_request(session, (NWS_API_STATIONS
											  + station_id
											  + '/observations'))
	response = observations_data.get('response')
	retrieved_at = observations_data.get('retrieved_at')
	observations = []
	for feature in response.get('features', {}):
		observations.append(process_observations_data(feature, retrieved_at, station_id))
	return observations


@display_spinner('Getting latest station observations...')
def get_latest_observations(
	session: CachedSession,
	station_id: str
) -> Observation:
	observations_data = api_request(session, (NWS_API_STATIONS
											  + station_id
											  + '/observations/latest'))
	response = observations_data.get('response')
	retrieved_at = observations_data.get('retrieved_at')
	return process_observations_data(response, retrieved_at, station_id)


@display_spinner('Getting station observations at the given time...')
def get_observations_at_time(
	session: CachedSession,
	station_id: str,
	timestamp: str
) -> Observation:
	observations_data = api_request(session, (NWS_API_STATIONS
											  + station_id
											  + '/observations/'
											  + timestamp))
	response = observations_data.get('response')
	retrieved_at = observations_data.get('retrieved_at')
	return process_observations_data(response, retrieved_at, station_id)


@display_spinner('Getting extended forecast for location...')
def get_extended_forecast(
	session: CachedSession,
	location: Location
) -> Forecast:
	forecast_data = api_request(session, location.forecast_extended_url)
	response = forecast_data.get('response')
	retrieved_at = forecast_data.get('retrieved_at')
	return process_forecast_data(response, retrieved_at, location)


@display_spinner('Getting hourly forecast for location...')
def get_hourly_forecast(
	session: CachedSession,
	location: Location
) -> Forecast:
	forecast_data = api_request(session, location.forecast_hourly_url)
	response = forecast_data.get('response')
	retrieved_at = forecast_data.get('retrieved_at')
	return process_forecast_data(response, retrieved_at, location)
