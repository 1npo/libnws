"""Get any needed data from the NWS API endpoints, clean it, and standardize it
"""

import os
import json
from dataclasses import dataclass, asdict, is_dataclass
from pathlib import Path
from rich.console import Console
from rich.pretty import pprint
from requests_cache import CachedSession
from libnws.repository.memory import InMemoryRepository
from libnws.repository.sqlite import SQLiteRepository
from libnws.render.decorators import display_spinner
from libnws.api.get_alerts import *
from libnws.api.get_aviation import *
from libnws.api.get_enums import *
from libnws.api.get_glossary import *
from libnws.api.get_location import *
from libnws.api.get_offices import *
from libnws.api.get_products import *
from libnws.api.get_radar import *
from libnws.api.get_stations import *
from libnws.api.get_weather import *
from libnws.api.get_zones import *
from libnws.model import *
logger = logging.getLogger(__name__)


def get_all_nws_data(session: CachedSession, address: str) -> dict:
	"""Get sample weather data for testing
	"""
	
	# weather
	location_data = get_location(session, address)

	# stations
	local_stations_data = get_stations_near_location(session, location_data)
	nearest_station = local_stations_data[1].station_id
	observations_latest = get_latest_observations(session, nearest_station)
	observations_all = get_all_observations(session, nearest_station)
	observations_at_time = get_observations_at_time(session, 'KBOS', '2024-08-19T18:54:00+00:00')
	forecast_extended = get_extended_forecast(session, location_data)
	forecast_hourly = get_hourly_forecast(session, location_data)

	# radar
	radar_servers = get_radar_servers(session)
	radar_server = get_radar_server(session, 'ldm2')
	radar_stations = get_radar_stations(session)
	radar_station = get_radar_station(session, 'KMVX')
	radar_station_alarms = get_radar_station_alarms(session, 'KHPX')
	radar_queue = get_radar_queue(session, 'rds', 'KBOX')

	# alerts
	alerts = get_alerts_by_area(session, 'FL')
	alert_counts = get_alert_counts(session)

	# products
	product_types = get_product_types(session)
	product_types_by_location = get_product_types_by_location(session, 'BGM')
	product_locations = get_product_locations(session)
	product_locations_by_type = get_product_locations_by_type(session, 'RVF')
	products = get_products(session)
	products_by_type = get_products_by_type(session, 'RR2')
	products_by_type_and_location = get_products_by_type_and_location(session, 'ADA', 'SRH')
	product = get_product(session, '5359e496-498b-40b9-bae6-0f0dcddc87a2')

	# zones
	zone = get_zone(session, 'county', 'AKC013')
	zones = get_zones(session, 'coastal')
	zone_stations = get_zone_stations(session, 'TXZ120')
	zone_observations = get_zone_observations(session, 'TNZ061')
	zone_forecast = get_zone_forecast(session, 'TNZ061')

	# enums
	valid_zones = get_valid_zones(session)
	valid_forecast_offices = get_valid_forecast_offices(session)

	# offices
	office = get_office(session, 'BOX')
	office_headlines = get_office_headlines(session, 'BOX')
	office_headline = get_office_headline(session, 'BOX', 'a194056daf964fce962ec37e0d6dcdef')

	# aviation
	sigmets = get_all_sigmets(session)
	atsu_sigmets = get_all_atsu_sigmets(session, 'KKCI')
	atsu_date_sigmets = get_all_atsu_sigmets_by_date(session, 'KKCI', '2024-08-18')
	sigmet = get_sigmet(session, 'KKCI', '2024-08-18', '0455')
	cwsu = get_cwsu(session, 'ZOB')
	cwas = get_cwas(session, 'ZOB')
	cwa = get_cwa(session, 'ZOB', '2024-08-17', 101)

	# glossary
	glossary = get_glossary(session)

	weather_data = {
		'location_data':					location_data,
		'local_stations_data':				local_stations_data,
		'nearest_station':					nearest_station,
		'observations_latest':				observations_latest,
		'observations_all':					observations_all,
		'observations_at_time':				observations_at_time,
		'forecast_extended':				forecast_extended,
		'forecast_hourly':					forecast_hourly,
		'alerts':							alerts,
		'alert_counts':						alert_counts,
		'radar_server':						radar_server,
		'radar_servers':					radar_servers,
		'radar_station':					radar_station,
		'radar_stations':					radar_stations,
		'radar_station_alarms':				radar_station_alarms,
		'radar_queue':						radar_queue,
		'product_types':					product_types,
		'product_types_by_location':		product_types_by_location,
		'product_locations':				product_locations,
		'product_locations_by_type':		product_locations_by_type,
		'products':							products,
		'products_by_type':					products_by_type,
		'products_by_type_and_location':	products_by_type_and_location,
		'product':							product,
		'zone':								zone,
		'zones':							zones,
		'zone_stations':					zone_stations,
		'zone_observations':				zone_observations,
		'zone_forecast':					zone_forecast,
		'valid_zones':						valid_zones,
		'valid_forecast_offices':			valid_forecast_offices,
		'office':							office,
		'office_headlines':					office_headlines,
		'office_headline':					office_headline,
		'sigmets':							sigmets,
		'atsu_sigmets':						atsu_sigmets,
		'atsu_date_sigmets':				atsu_date_sigmets,
		'sigmet':							sigmet,
		'cwas':								cwas,
		'cwa':								cwa,
		'cwsu':								cwsu,
		'glossary':							glossary,
	}
	weather_data_sorted = {k: v for k, v in sorted(weather_data.items(), key=lambda i: i[0])}
	return weather_data_sorted


def nws_data_to_json(session: CachedSession, address: str):
	nws_data = get_all_nws_data(session, address)
	output_path = Path(os.path.expanduser('~')) / 'nws_data'
	Path(output_path).mkdir(parents=True, exist_ok=True)
	for name, data in nws_data.items():
		output_file = output_path / f'nws_raw_{name}.json'
		if is_dataclass(data):
			data = asdict(data)
		with open(output_file, 'w') as f:
			f.write(json.dumps(data, default=str, indent=4))
		logger.success(f'Wrote {name} to {output_file}')


def pprint_raw_nws_data(session: CachedSession, address: str):
	nws_data = get_all_nws_data(session, address)
	console = Console()
	data_item_filter = [
		'alerts',
		'sigmet',
		'location_data',
		'office',
		'product',
		'radar_station',
		'local_stations_data',
		'observations_latest',
		'zone',
	]
	for name, data in nws_data.items():
		if name in ('zone_forecast'):
			console.print(f'{name}\n{"=" * len(name)}', style='bold red')
			pprint(data)


def test_memory_repository(session: CachedSession, address: str):
	nws_data = get_all_nws_data(session, address)
	repo = InMemoryRepository()
	test_item_alerts = nws_data.get('alerts')
	test_item_sigmet = nws_data.get('sigmet')
	test_item_location = nws_data.get('location_data')
	test_item_office = nws_data.get('office')
	test_item_product = nws_data.get('product')
	test_item_radar_station = nws_data.get('radar_station')
	test_item_stations = nws_data.get('local_stations_data')
	test_item_observation = nws_data.get('observations_latest')
	test_item_zones = nws_data.get('zone')

	items = [
		test_item_alerts,
		test_item_sigmet,
		test_item_location,
		test_item_office,
		test_item_product,
		test_item_radar_station,
		test_item_stations,
		test_item_observation,
		test_item_zones,
	]

	'''
	for item in items:
		if isinstance(item, list):
			for i in item:
				repo.create(i)
				logger.success(f'Added item to in-memory repo: {i=}')
		else:
			repo.create(item)
			logger.success(f'Added item to in-memory repo: {item=}')			
	'''


	for i in range(1, 5):
		pprint(repo.create(test_item_location))

	#pprint(f'Printing ALL')
	#pprint(repo.get_all())
	#pprint(f'Printing ONE')
	pprint(repo.filter_by({'city': 'Winchester'}))


def test_sqlite_repository(session: CachedSession, address: str):
	repo = SQLiteRepository(sqlite_path='C:/Users/Nick/Downloads/nwsc.db')
	test_addr1 = '3121 S Las Vegas Blvd, Las Vegas, NV 89109'
	test_addr2 = '589 Mt. Auburn St., Watertown, MA 02472'
	test_addr3 = '600 Bennington St. Boston, MA 02128'
	test_addr4 = '2 15th St NW, Washington, DC 20024'
	test_addr5 = '3001 Connecticut Ave NW, Washington, DC 20008'
	test_addrs = [
		#test_addr1,
		test_addr2,
		test_addr3,
		test_addr4,
		test_addr5,
	]
	#for addr in test_addrs:
	#	location = get_location(session, addr)
	#	created = repo.create('locations', location)
	#	print(f'Created location record (row_id = {created})')
	
	locations = repo.get_all('locations', Location)
	pprint(locations)

	deleted = repo.delete('locations', {'city': 'Watertown Town'})
	if deleted:
		print(f'Deleted record')
	else:
		print(f'Record not found!')
	
	winchester_filter = {'city': 'Winchester'}
	winchester_location = repo.filter_by('locations', Location, winchester_filter)[0]
	winchester_location.grid_x = 69
	winchester_location.grid_y = 420
	updated = repo.update('locations', winchester_location, winchester_filter)
	if updated:
		print(f'Updated record')
	else:
		print(f'Failed to update record!')

	winchester_location = repo.filter_by('locations', Location, winchester_filter)[0]
	print(winchester_location)

	locations = repo.get_all('locations', Location)
	pprint(locations)