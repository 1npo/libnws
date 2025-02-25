__version__ = '0.0.0'


BUG_REPORT_MESSAGE = (
    'This is an unexpected result and probably a bug. Please report it '
    'on GitHub at https://github.com/1npo/nwsc/issues.'
)


import os
import sys
import argparse
import logging
import pandas as pd
from pathlib import Path
from datetime import datetime
from requests_cache import CachedSession, SQLiteCache, FileCache, NEVER_EXPIRE
from libnws.config import ConfigManager
from libnws.render.decorators import display_spinner
from libnws.render.pprint_raw import (
    pprint_raw_nws_data,
	nws_data_to_json,
	test_memory_repository,
	test_sqlite_repository,
	)
from libnws.render.rich_print import (
    rich_print_current_conditions,
	rich_print_extended_forecast,
	rich_print_settings,
	rich_print_overview,
	)
logging.basicConfig(format='%(asctime)s : %(levelname)-8s : %(name)s : %(message)s',
					datefmt='%Y-%m-%d %I:%M%p',
					level=logging.INFO)
logger = logging.getLogger(__name__)


class LogFilter:
    def __init__(self, level):
        self.level = level
	
    def __call__(self, record):
        levelno = logger.level(self.level).no
        return record["level"].no >= levelno


log_filter = LogFilter('INFO')
LOG_FMT_TERM = '[<level>{level: <8}</level>] <level>{message}</level>'
logger.remove()
logger.add(sys.stderr, format=LOG_FMT_TERM, filter=log_filter, level=0)


parser = argparse.ArgumentParser(prog='nws',
								 formatter_class=argparse.RawDescriptionHelpFormatter,
								 description=f'nws v{__version__} - Lightweight NWS API Client for the Terminal')
parser.add_argument('--debug', action='store_true', help='Display debugging information in the terminal')
parser.add_argument('--save', action='store_true', help='Save the current observations to an Excel file')
parser_location = parser.add_mutually_exclusive_group()
parser_location.add_argument('--address', action='store', type=str, help='Get the weather from the station nearest to this address (default: address in user settings)')
parser_location.add_argument('--station', action='store', type=str, help='Get the weather from this 4-letter station ID (default: nearest station to the address in user settings)')
subparsers = parser.add_subparsers(dest='command')
parser_current = subparsers.add_parser('current', help='Get the current observations')
parser_overview = subparsers.add_parser('overview', help='Get the current observations plus the 3 day forecast')
parser_forecast = subparsers.add_parser('forecast', help='Get the weather forecast')
parser_forecast.add_argument('forecast-type', nargs='?', choices=['3day', '7day', 'hourly'], help='The type of forecast to get (default: 3day)')
parser_forecast.add_argument('--save', action='store_true', help='Save the forecast to an Excel file')
parser_set = subparsers.add_parser('set', help='Change a setting')
parser_set.add_argument('set', action='store', type=str, help='Change the value of this setting')
parser_set.add_argument('value', action='store', type=str, help='Change the setting to this value')
parser_get = subparsers.add_parser('get', help='Display the current value of a setting (or display all settings of none specified)')
parser_get.add_argument('get', action='store', type=str, nargs='?', default=None, help='Print the current value of this setting (or print all if setting not specified)')


def df_to_file(
	config: ConfigManager,
	name: str,
	df: pd.DataFrame,
	index=False
):
	"""Save the given dataframe to a file
	
	:param config: An instance of ConfigManager
	:param name: The name of the export (eg 'current', 'overview', 'forecast')
	:param df: The dataframe to save to a file
	"""
	output_dir = config.get('exports_dir')
	if not os.path.isfile(output_dir):
		Path(output_dir).mkdir(parents=True, exist_ok=True)

	timestamp = datetime.now().strftime('%Y-%m-%d_%I%M%S%p')
	output_file = f'nws_api_export_{name}_{timestamp}.xlsx'
	output_path = os.path.join(output_dir, output_file)
	with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
		df.to_excel(writer, index=index, sheet_name=name)
	logger.info(f'Saved {name} to file: {output_path}')


def main():
	config = ConfigManager()
	params, other = parser.parse_known_args()
	address = params.address if params.address else config.get('address')
	backend = SQLiteCache()
	session = CachedSession('nwsc_cache',
						 	backend=backend,
							use_cache_dir=True,
							cache_control=True,
							expire_after=NEVER_EXPIRE,
							)
	with session:
		if params.debug:
			log_filter.level = 'DEBUG'
		
		if params.command == 'get':
			if not params.get:
				rich_print_settings(config.get_all())
			else:
				print(f'{params.get} = {config.get(params.get)}')
			exit(0)

		if params.command == 'set':
			config.set(params.set, params.value)
			logger.info(f'Set "{params.set}" to "{params.value}"')
			exit(0)
		
		if params.command == 'overview':
			#forecast_df = extended_forecast_to_dforecast_hourlyf(address, periods=6)
			#current_df = current_observations_to_df(address)
			#rich_print_overview(current_df.iloc[0], forecast_df)
			#if params.save:
			#	df_to_file(config, 'current', current_df)
			#	df_to_file(config, 'forecast', forecast_df)
			exit(0)

		if params.command == 'forecast':
			#match params.forecast_type:
			#	case 'hourly':
			#		forecast_df = hourly_forecast_to_df(address)
			#	case '7day':
			#		forecast_df = extended_forecast_to_df(address)
			#	case '3day':
			#		forecast_df = extended_forecast_to_df(address, periods=6)
			#	case _:
			#		forecast_df = extended_forecast_to_df(address, periods=6)
			#rich_print_extended_forecast(forecast_df)
			#if params.save:
			#	df_to_file(config, 'forecast', forecast_df)
			exit(0)

		if params.command in (None, 'current'):
			#current_df = current_observations_to_df(address)
			#rich_print_current_conditions(current_df.iloc[0])
			#if params.save:
			#	df_to_file(config, 'observations', current_df.iloc[0], index=True)
			test_addr1 = '3121 S Las Vegas Blvd, Las Vegas, NV 89109'
			test_addr2 = '589 Mt. Auburn St., Watertown, MA 02472'
			test_addr3 = '600 Bennington St. Boston, MA 02128'
			test_addr4 = '2 15th St NW, Washington, DC 20024'
			test_addr5 = '3001 Connecticut Ave NW, Washington, DC 20008'
			#pprint_raw_nws_data(session, test_addr5)
			#nws_data_to_json(session, test_addr5)
			#test_memory_repository(session, test_addr1)
			test_sqlite_repository(session, test_addr1)
			exit(0)
