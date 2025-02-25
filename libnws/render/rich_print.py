from typing import Optional

import pandas as pd
from rich import print, box
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.columns import Columns


# See: https://gist.github.com/neelabalan/33ab34cf65b43e305c3f12ec6db05938
def df_to_table(
	pandas_dataframe: pd.DataFrame,
	rich_table: Table,
	show_index: bool = True,
	index_name: Optional[str] = None,
	add_row_kwargs: dict = {},
	add_column_kwargs: dict = {},
) -> Table:
	"""Convert a pandas.DataFrame obj into a rich.Table obj.

	This structure is expected for add_row_kwargs: {'param1': 'value, 'paramN': 'value'}.
	This structure is expected for add_column_kwargs: {'column_name': {'param1': 'value', 'paramN': 'value'}}.
	If special column name '__all__' is used in add_column_kwargs, then the  given kwargs will be applied to
	all columns.

	Args:
		pandas_dataframe (DataFrame): A Pandas DataFrame to be converted to a rich Table.
		rich_table (Table): A rich Table that should be populated by the DataFrame values.
		show_index (bool): Add a column with a row count to the table. Defaults to True.
		index_name (str, optional): The column name to give to the index column. Defaults to None, showing no value.
		add_column_kwargs (dict, optional): Any additional keyword arguments to pass to `table.add_column()`.
		add_row_kwargs (dict, optional): Any additional keyword arguments to pass to `table.add_row()`.
	Returns:
		Table: The rich Table instance passed, populated with the DataFrame values."""

	if show_index:
		index_name = str(index_name) if index_name else ""
		
		# Apply additional keyword arguments provided by user
		kwargs = {}
		if add_column_kwargs.get('ALL'):
			kwargs = add_column_kwargs['ALL']

		rich_table.add_column(index_name, **kwargs)

	for column in pandas_dataframe.columns:
		# Apply additional keyword arguments provided by user
		kwargs = {}
		if add_column_kwargs.get('ALL'):
			kwargs.update(add_column_kwargs['ALL'])
		if column in add_column_kwargs.keys():
			kwargs.update(add_column_kwargs[column])

		rich_table.add_column(str(column), **kwargs)

	for index, value_list in enumerate(pandas_dataframe.values.tolist()):
		row = [str(index)] if show_index else []
		row += [str(x) for x in value_list]
		rich_table.add_row(*row, **add_row_kwargs)

	return rich_table


def format_weather_value(
	field: str,
	value: str
) -> str:
	if pd.isna(value):
		return None
	
	match field[-3:]:
		case '_pc':
			return f'{round(value, 2)}%'
		case '_pa':
			return f'{int(value)} Pa',
		case '_mi':
			return f'{round(value, 2)} mi',

	match field[-5:]:
		case '_m_hr':
			return f'{int(value)} mph',

	match field[-6:]:
		case '_deg_f':
			return f'{int(value)}°F',
		case '_deg_c':
			return f'{int(value)}°C',
		case '_1h_mm':
			return f'{round(value, 2)} mm',

	return value


def rich_print_current_conditions(
	current_s: pd.Series,
	station_panel: bool = True
):
	"""
	"""

	# Rename fields for presentation in the weather panel
	weather_field_names = {
		'text_description': 		'conditions',
		'cloud_layers_amt':			'clouds',
		'temperature_deg_f':		'temp',
		'dew_point_deg_f':			'dew point',
		'wind_chill_deg_f':			'wind chill',
		'wind_speed_str':			'wind speed',
		'relative_humidity_pc':		'humidity',
		'barometric_pressure_pa':	'air pressure',
		'visibility_mi':			'visibility',
		'precip_last_1h_mm':		'precip last hour',
	}

	table_weather = Table(box=None)
	table_weather.add_column(justify='right')
	table_weather.add_column(justify='left')

	for old_field, new_field in weather_field_names.items():
		weather_value = format_weather_value(old_field, current_s[old_field])
		if isinstance(weather_value, tuple):
			weather_value = weather_value[0]

		table_weather.add_row(Text(new_field, style='bold indian_red1'), f'{weather_value}')

	panel_weather = Panel(table_weather,
						  title=Text('current weather', style='bold cornflower_blue'),
						  border_style='cornflower_blue',
						  expand=False)
	
	# Display names and values for the station panel
	station_field_values = {
		'observed by':	f'{current_s["station_name"]} ({current_s["station_id"]})',
		'observed at':	current_s['observed_at'].strftime('%Y-%m-%d %I:%M:%S %p %Z'),
	}

	table_station = Table(box=None)
	table_station.add_column(justify='right')
	table_station.add_column(justify='left')

	for field, value in station_field_values.items():
		table_station.add_row(Text(field, style='bold indian_red1'), value)

	panel_station = Panel(table_station,
						  title=Text('station', style='bold cornflower_blue'),
						  border_style='cornflower_blue',
						  expand=False)

	if station_panel:
		print()
		print(Columns([panel_weather, panel_station]))
	else:
		print(panel_weather)


def rich_print_extended_forecast(
	df: pd.DataFrame,
	station_panel: bool = True
) -> dict:
	"""
	"""
	df['wind_speed'] = df['wind_speed'] + ' ' + df['wind_direction']
	station_id = df['station_id'].iloc[0]
	station_name = df['station_name'].iloc[0]
	generated_at = df['forecast_generated_at'].iloc[0]
 
	## Get needed fields from dataframe
	extended_forecast_fields = {
		'period_name':				'period',
		'period_forecast_short':	'forecast',
		'wind_speed':				'wind',
		'temperature_deg_f':		'temp',
		'humidity_pc':				'humidity',
		'precipitation_pc':			'precip',
	}
	available_fields = [f for f in extended_forecast_fields if f in df.columns]
	df = df[available_fields]
	df = df.rename(columns=extended_forecast_fields)
	df['temp'] = df['temp'].astype(str) + '°F'
	df['#'] = range(1, len(df.index)+1)
	df = df[['#'] + [c for c in df.columns if c != '#']]
	for field in ['humidity', 'precip']:
		if field in df:
			df[field] = df[field].astype(int)
			df[field] = df[field].astype(str) + '%'

	## Keyword arguments to use on add_column when converting dataframe to rich table
	kwargs = {
		'temp': 	{'justify': 'center'},
		'humidity': {'justify': 'center'},
		'precip':	{'justify': 'center'},
	}

	table_weather = Table(box=box.SIMPLE, header_style='indian_red1')#box.ROUNDED, show_lines=True)
	table_weather = df_to_table(df,
					 			table_weather,
					 			show_index=False,
					 			add_column_kwargs=kwargs)
	
	panel_weather = Panel(table_weather,
						  title=Text('forecast', style='bold cornflower_blue'),
						  border_style='cornflower_blue',
						  expand=False)
	
	# Display names and values for the station panel
	station_field_values = {
		'generated by':	f'{station_name} ({station_id})',
		'generated at':	generated_at.strftime('%Y-%m-%d %I:%M:%S %p %Z'),
	}

	table_station = Table(box=None)
	table_station.add_column(justify='right')
	table_station.add_column(justify='left')

	for field, value in station_field_values.items():
		field = Text(field)
		field.stylize('bold indian_red1')

		table_station.add_row(field, value)

	panel_station = Panel(table_station,
					   	  title=Text('station', style='bold cornflower_blue'),
						  border_style='cornflower_blue',
						  expand=False)

	print()
	print(panel_weather)

	if station_panel:
		print()
		print(panel_station)


def rich_display_hourly_forecast(
	forecast_df
):
	raise NotImplementedError()


def rich_print_overview(
	current_s: pd.Series,
	forecast_df: pd.DataFrame
):
	# TODO: Do this better
	rich_print_current_conditions(current_s, station_panel=False)
	rich_print_extended_forecast(forecast_df)


def rich_print_settings(
	settings: dict
):
	"""
	"""
	table = Table(box=box.SIMPLE, header_style='indian_red1')
	table.add_column('setting')
	table.add_column('value')

	for setting in settings:
		table.add_row(*setting)

	panel = Panel(table,
				  title=Text('settings', style='bold cornflower_blue'),
				  border_style='cornflower_blue',
				  expand=False)

	print()
	print(panel)
