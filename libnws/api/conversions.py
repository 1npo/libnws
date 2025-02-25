"""
"""

import logging
logger = logging.getLogger(__name__)


def convert_temperatures(data: dict) -> dict:
	"""Ensure that temperatures are represented in both metric and imperial"""
	new_data = {}
	for field, value in data.items():
		new_data[field] = value
		if field[-2:] == '_c':
			field_f = f'{field[:-2]}_f'
			if field_f not in data:
				new_data[field_f] = None
				if value:
					new_data[field_f] = (value * 9/5) + 32
		if field[-2:] == '_f':
			field_c = f'{field[:-2]}_c'
			if field_c not in data:
				new_data[field_c] = None
				if value:
					new_data[field_c] = (value - 32) * 5/9
	return new_data


def convert_speeds(data: dict) -> dict:
	"""Ensure that speeds are represented in both metric and imperial"""
	new_data = {}
	for field, value in data.items():
		new_data[field] = value
		if field[-4:] == '_kmh':
			field_mph = f'{field[:-4]}_mph'
			if field_mph not in data:
				new_data[field_mph] = None
				if value:
					new_data[field_mph] = value / 1.609344
		if field[-4:] == '_mph':
			field_kmph = f'{field[:-4]}_kmh'
			if field_kmph not in data:
				new_data[field_kmph] = None
				if value:
					new_data[field_kmph] = value * 1.609344
	return new_data


def convert_distances(data: dict) -> dict:
	"""Ensure that distances are represented in both metric and imperial"""
	new_data = {}
	for field, value in data.items():
		new_data[field] = value
		if field[-2:] == '_m':
			field_miles = f'{field[:-2]}_mi'
			if field_miles not in data:
				new_data[field_miles] = None
				if value:
					new_data[field_miles] = value / 1609.344
		if field[-3:] == '_mi':
			field_meters = f'{field[:-3]}_m'
			if field_meters not in data:
				new_data[field_miles] = None
				if value:
					new_data[field_meters] = value * 1609.344
	return new_data


def convert_pressures(data: dict) -> dict:
	"""Ensure that pressures are represented in both metric and imperial"""
	new_data = {}
	for field, value in data.items():
		new_data[field] = value
		if field[-3:] == '_pa':
			field_inhg = f'{field[:-3]}_inhg'
			if field_inhg not in data:
				new_data[field_inhg] = None
				if value:
					new_data[field_inhg] = value / 3386.39
		if field[-5:] == '_inhg':
			field_pa = f'{field[:-5]}_pa'
			if field_pa not in data:
				if value:
					new_data[field_pa] = value * 3386.39
	return new_data


# See: http://tamivox.org/dave/compass/
def convert_directions(data: dict) -> dict:
	"""Add wind direction string on a 16-point compass"""
	if data.get('wind_direction_deg_ang'):
		if ((0 <= data['wind_direction_deg_ang'] <= 22.4) or
	  		data['wind_direction_deg_ang'] == 360):
			data['wind_direction_compass'] = 'N'
		elif 22.5 <= data['wind_direction_deg_ang'] <= 44.9:
			data['wind_direction_compass'] = 'NNE'
		elif 45 <= data['wind_direction_deg_ang'] <= 67.4:
			data['wind_direction_compass'] = 'NE'
		elif 67.5 <= data['wind_direction_deg_ang'] <= 89.9:
			data['wind_direction_compass'] = 'ENE'
		elif 90 <= data['wind_direction_deg_ang'] <= 112.4:
			data['wind_direction_compass'] = 'E'
		elif 112.5 <= data['wind_direction_deg_ang'] <= 134.9:
			data['wind_direction_compass'] = 'ESE'
		elif 135 <= data['wind_direction_deg_ang'] <= 157.4:
			data['wind_direction_compass'] = 'SE'
		elif 157.5 <= data['wind_direction_deg_ang'] <= 179.9:
			data['wind_direction_compass'] = 'SSE'
		elif 180 <= data['wind_direction_deg_ang'] <= 202.4:
			data['wind_direction_compass'] = 'S'
		elif 202.5 <= data['wind_direction_deg_ang'] <= 224.9:
			data['wind_direction_compass'] = 'SSW'
		elif 225 <= data['wind_direction_deg_ang'] <= 247.4:
			data['wind_direction_compass'] = 'SW'
		elif 247.5 <= data['wind_direction_deg_ang'] <= 269.9:
			data['wind_direction_compass'] = 'WSW'
		elif 270 <= data['wind_direction_deg_ang'] <= 292.4:
			data['wind_direction_compass'] = 'W'
		elif 292.5 <= data['wind_direction_deg_ang'] <= 314.9:
			data['wind_direction_compass'] = 'WNW'
		elif 315 <= data['wind_direction_deg_ang'] <= 337.4:
			data['wind_direction_compass'] = 'NW'
		elif 337.5 <= data['wind_direction_deg_ang'] <= 359.9:
			data['wind_direction_compass'] = 'NNW'
		else:
			data['wind_direction_compass'] = None
	else:
		if 'wind_direction_deg_ang' in data:
			data['wind_direction_compass'] = None
	return data


def round_floats(data: dict) -> dict:
	for k, v in data.items():
		if isinstance(v, float):
			data[k] = round(v, 2)
	return data


def convert_measures(data: dict) -> dict:
	data = convert_temperatures(data)
	data = convert_speeds(data)
	data = convert_distances(data)
	data = convert_pressures(data)
	data = convert_directions(data)
	data = round_floats(data)
	return data
