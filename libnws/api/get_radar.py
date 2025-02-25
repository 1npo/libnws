from typing import List
from datetime import datetime
from requests_cache import CachedSession
from libnws.render.decorators import display_spinner
from libnws.api.get_weather import process_measurement_values
from libnws.api.conversions import convert_measures
from libnws.api.api_request import api_request, parse_timestamp
from libnws.api import (
	NWS_API_RADAR_SERVERS,
    NWS_API_RADAR_STATIONS,
	NWS_API_RADAR_QUEUES,
)
from libnws.model.radar import (
	RadarStation,
	RadarStationAlarm,
	RadarQueueItem,
	RadarPathLoss,
	RadarDataAcquisition,
	RadarAdaptation,
	RadarPerformance,
	RadarServer,
	NetworkInterface,
)


def process_radar_station_rda_data(radar_station_data: dict) -> RadarDataAcquisition:
	rda_data = radar_station_data.get('properties', {}).get('rda', {})
	rda_dict = {}
	rda = None
	if rda_data and isinstance(rda_data, dict):
		rda_dict.update({
			'refreshed_at':				parse_timestamp(rda_data.get('timestamp')),
			'reporting_host':			rda_data.get('reportingHost', {}),
			'resolution_version':		(rda_data.get('properties', {})
												 .get('resolutionVersion')),
			'nexrad_l2_path':			(rda_data.get('properties', {})
												 .get('nl2Path')),
			'volume_coverage_pattern':	(rda_data.get('properties', {})
												 .get('volumeCoveragePattern')),
			'control_status':			(rda_data.get('properties', {})
												 .get('controlStatus')),
			'build_number':				rda_data.get('properties', {}).get('buildNumber'),
			'alarm_summary':			(rda_data.get('properties', {})
												 .get('alarmSummary')),
			'mode':						rda_data.get('properties', {}).get('mode'),
			'generator_state':			(rda_data.get('properties', {})
												 .get('generatorState')),
			'super_resolution_status':	(rda_data.get('properties', {})
												 .get('superResolutionStatus')),
			'operability_status':		(rda_data.get('properties', {})
												 .get('operabilityStatus')),
			'status':					rda_data.get('properties', {}).get('status'),
		})
		field_map = {
			'averageTransmitterPower': 				'average_tx_power',
			'reflectivityCalibrationCorrection':	'reflectivity_calibration_correction',
		}
		expected_types = {
			'averageTransmitterPower': 				'wmoUnit:W',
			'reflectivityCalibrationCorrection':	'wmoUnit:dB',
		}
		rda_measures = rda_data.get('properties', {})
		rda_dict.update(process_measurement_values(rda_measures,
												   field_map,
												   expected_types))
		rda = RadarDataAcquisition(**rda_dict)
	return rda


def process_radar_station_performance_data(radar_station_data: dict) -> RadarPerformance:
	performance_data = radar_station_data.get('properties', {}).get('performance')
	performance_dict = {}
	performance = None
	if performance_data and isinstance(performance_data, dict):
		performance_dict.update({
			'refreshed_at':					performance_data.get('timestamp'),
			'performance_checked_at':		(performance_data
												.get('properties', {})
												.get('performanceCheckTime')),
			'reporting_host':				performance_data.get('reportingHost'),
			'ntp_status':					(performance_data
												.get('properties', {})
												.get('ntp_status')),
			'command_channel':				(performance_data
												.get('properties', {})
												.get('commandChannel')),
			'linearity':					(performance_data
												.get('properties', {})
												.get('linearity')),
			'power_source':					(performance_data
												.get('properties', {})
												.get('powerSource')),
			'transmitter_recycle_count':	(performance_data
												.get('properties', {})
												.get('transmitterRecycleCount')),
			'transitional_power_source':	(performance_data
												.get('properties', {})
												.get('transitionalPowerSource')),
			'elevation_encoder_light':		(performance_data
												.get('properties', {})
												.get('elevationEncoderLight')),
			'azimuth_encoder_light':		(performance_data
												.get('properties', {})
												.get('azimuthEncoderLight')),
		})
		field_map = {
			'fuelLevel': 						'fuel_level',
			'dynamicRange': 					'dynamic_range',
			'transmitterPeakPower': 			'transmitter_peak_power',
			'transmitterImbalance': 			'transmitter_imbalance',
			'transmitterLeavingAirTemperature': 'transmitter_leaving_air_temp',
			'shelterTemperature': 				'shelter_temp',
			'radomeAirTemperature': 			'radome_air_temp',
			'horizontalNoiseTemperature': 		'horizontal_noise_temp',
			'horizontalDeltadbZ0': 				'horizontal_delta',
			'verticalDeltadbZ0': 				'vertical_delta',
			'receiverBias': 					'receiver_bias',
			'horizontalShortPulseNoise': 		'horizontal_short_pulse_noise',
			'horizontalLongPulseNoise': 		'horizontal_long_pulse_noise',
		}
		expected_types = {
			'fuelLevel': 						'wmoUnit:percent',
			'dynamicRange': 					'wmoUnit:dB',
			'transmitterPeakPower': 			'wmoUnit:kW',
			'transmitterImbalance': 			'wmoUnit:dB',
			'transmitterLeavingAirTemperature': 'wmoUnit:degC',
			'shelterTemperature': 				'wmoUnit:degC',
			'radomeAirTemperature': 			'wmoUnit:degC',
			'horizontalNoiseTemperature': 		'wmoUnit:degC',
			'horizontalDeltadbZ0': 				'wmoUnit:dB',
			'verticalDeltadbZ0': 				'wmoUnit:dB',
			'receiverBias': 					'wmoUnit:dB',
			'horizontalShortPulseNoise': 		'wmoUnit:dB_m-1',
			'horizontalLongPulseNoise': 		'wmoUnit:dB_m-1',
		}
		performance_measures = performance_data.get('properties', {})
		performance_dict.update(process_measurement_values(performance_measures,
														   field_map,
														   expected_types))
		performance_dict = convert_measures(performance_dict)
		performance = RadarPerformance(**performance_dict)
	return performance


def process_radar_station_adaptation_data(radar_station_data: dict) -> RadarAdaptation:
	adaptation_data = radar_station_data.get('properties', {}).get('adaptation')
	adaptation_dict = {}
	adaptation = None
	if adaptation_data and isinstance(adaptation_data, dict):
		path_loss_dict = {
			'wg04_circulator': (
				adaptation_data.get('pathLossWG04Circulator')),
			'wg02_harmonic_filter':	(
				adaptation_data.get('pathLossWG02HarmonicFilter')),
			'wg06_spectrum_filter': (
				adaptation_data.get('pathLossWG06SpectrumFilter')),
			'ifd_rif_anti_alias_filter': (
				adaptation_data.get('pathLossIFDRIFAntiAliasFilter')),
			'ifd_burst_anti_alias_filter': (
				adaptation_data.get('pathLossIFDBurstAntiAliasFilter')),
			'a6_arc_detector': (
				adaptation_data.get('pathLossA6ArcDetector')),
			'transmitter_coupler_coupling': (
				adaptation_data.get('pathLossTransmitterCouplerCoupling')),
			'vertical_f_heliax_to_4at16': (
				adaptation_data.get('pathLossVerticalIFHeliaxTo4AT16')),
			'horizontal_f_heliax_to_4at17': (
				adaptation_data.get('pathLossHorzontalIFHeliaxTo4AT17')),
			'at4_attenuator': (
				adaptation_data.get('pathLossAT4Attenuator')),
			'waveguide_klystron_to_switch': (
				adaptation_data.get('pathLossWaveguideKlystronToSwitch')),
		}
		path_loss = RadarPathLoss(**path_loss_dict)
		adaptation_dict.update({
			'refreshed_at': (
				adaptation_data.get('timestamp')),
			'reporting_host': (
				adaptation_data.get('reportingHost')),
			'transmitter_frequency': (
				adaptation_data.get('transmitterFrequency')),
			'transmitter_power_data_watts_factor': (
				adaptation_data.get('transmitterPowerDataWattsFactor')),
			'antenna_gain_incl_radome': (
				adaptation_data.get('antennaGainIncludingRadome')),
			'coho_power_at_a1j4': (
				adaptation_data.get('cohoPowerAtA1J4')),
			'stalo_power_at_a1j2': (
				adaptation_data.get('staloPowerAtA1J2')),
			'horizontal_receiver_noise_long_pulse': (
				adaptation_data.get('horizontalReceiverNoiseLongPulse')),
			'horizontal_receiver_noise_short_pulse': (
				adaptation_data.get('horizontalReceiverNoiseShortPulse')),
			'transmitter_spectrum_filter_installed': (
				adaptation_data.get('transmitterSpectrumFilterInstalled')),
			'pulse_width_transmitter_out_long_pulse': (
				adaptation_data.get('pulseWidthTransmitterOutputLongPulse')),
			'pulse_width_transmitter_out_short_pulse': (
				adaptation_data.get('pulseWidthTransmitterOutputShortPulse')),
			'ame_noise_source_horizontal_excess_noise_ratio': (
				adaptation_data.get('ameNoiseSourceHorizontalExcessNoiseRatio')),
			'ame_horizontal_test_signal_power': (
				adaptation_data.get('ameHorzizontalTestSignalPower')),
			'path_loss': path_loss,
		})
		adaptation_dict = convert_measures(adaptation_dict)
		adaptation = RadarAdaptation(**adaptation_dict)
	return adaptation


def process_radar_station_data(
	radar_station_data: dict,
	retrieved_at: datetime
) -> RadarStation:
	station_coords = radar_station_data.get('geometry', {}).get('coordinates')
	if station_coords and isinstance(station_coords, list):
		station_lat = station_coords[0]
		station_lon = station_coords[1]
	data_rda = process_radar_station_rda_data(radar_station_data)
	data_performance = process_radar_station_performance_data(radar_station_data)
	data_adaptation = process_radar_station_adaptation_data(radar_station_data)
	station_dict = {
		'retrieved_at':						retrieved_at,
		'lat':								station_lat,
		'lon':								station_lon,
		'server_host':						(radar_station_data.get('properties', {})
															   .get('latency', {})
															   .get('host')),
		'reporting_host':					(radar_station_data.get('properties', {})
															   .get('latency', {})
															   .get('reportingHost')),
		'radar_station_id':					(radar_station_data.get('properties', {})
															   .get('id', {})),
		'name':								(radar_station_data.get('properties', {})
															   .get('name', {})),
		'station_type':						(radar_station_data.get('properties', {})
															   .get('stationType', {})),
		'timezone':							(radar_station_data.get('properties', {})
															   .get('timeZone')),
		'latency_nexrad_l2_last_received_at':	(parse_timestamp(radar_station_data
													.get('properties', {})
													.get('latency', {})
													.get('levelTwoLastReceivedTime'))),
		'max_latency_at':						(parse_timestamp(radar_station_data
													.get('properties', {})
													.get('latency', {})
													.get('maxLatencyTime'))),
		'radar_data_acquisition':				data_rda,
		'performance':							data_performance,
		'adaptation':							data_adaptation,
	}
	elevation_measures = radar_station_data.get('properties', {})
	station_dict.update(process_measurement_values(elevation_measures,
											  	   {'elevation': 'elevation'},
											  	   {'elevation': 'wmoUnit:m'}))
	station_dict = convert_measures(station_dict)
	for latency_type in ('current', 'average', 'max'):
		latency_measures = radar_station_data.get('properties', {}).get('latency', {})
		station_dict.update(
			process_measurement_values(latency_measures,
									   {latency_type: f'latency_{latency_type}'},
									   {latency_type: 'nwsUnit:s'}))
	return RadarStation(**station_dict)


def process_radar_server_data(radar_server_data: dict, retrieved_at: datetime) -> dict:
	server_dict = {
		'retrieved_at':						retrieved_at,
		'host':                  			radar_server_data.get('id'),
		'server_type':                  	radar_server_data.get('type'),
		'up_since':              			(parse_timestamp(radar_server_data
																.get('hardware', {})
																.get('uptime'))),
		'hardware_refreshed_at':   			(parse_timestamp(radar_server_data
																.get('hardware', {})
																.get('timestamp'))),
		'cpu':                   			(radar_server_data.get('hardware', {})
															  .get('cpuIdle')),
		'memory':                			(radar_server_data.get('hardware', {})
															  .get('memory')),
		'io_utilization':        			(radar_server_data.get('hardware', {})
															  .get('ioUtilization')),
		'disk':                  			(radar_server_data.get('hardware', {})
															  .get('disk')),
		'load_1':                			(radar_server_data.get('hardware', {})
															  .get('load1')),
		'load_5':                			(radar_server_data.get('hardware', {})
															  .get('load5')),
		'load_15':               			(radar_server_data.get('hardware', {})
															  .get('load15')),
		'command_last_executed':        	(radar_server_data.get('command', {})
															  .get('lastExecuted')),
		'command_last_executed_at': (
			parse_timestamp(radar_server_data.get('command', {})
											 .get('lastExecutedTime'))),
		'command_last_nexrad_data_at': (
			parse_timestamp(radar_server_data.get('command', {})
											 .get('lastNexradDataTime'))),
		'command_last_received': 			(radar_server_data.get('command', {})
															  .get('lastReceived')),
		'command_last_received_at': (
			parse_timestamp(radar_server_data.get('command', {})
											 .get('lastReceivedTime'))),
		'command_last_refreshed_at': (
			parse_timestamp(radar_server_data.get('command', {})
											 .get('timestamp'))),
		'ldm_refreshed_at': (
			parse_timestamp(radar_server_data.get('ldm', {})
											 .get('timestamp'))),
		'ldm_latest_product_at': (
			parse_timestamp(radar_server_data.get('ldm', {})
											 .get('latestProduct'))),
		'ldm_oldest_product_at': (
			parse_timestamp(radar_server_data.get('ldm', {})
											 .get('oldestProduct'))),
		'ldm_storage_size':             	(radar_server_data.get('ldm', {})
															  .get('storageSize')),
		'ldm_count':                    	(radar_server_data.get('ldm', {})
															  .get('count')),
		'is_ldm_active':                	(radar_server_data.get('ldm', {})
															  .get('active')),
		'is_server_active':             	radar_server_data.get('active'),
		'is_server_primary':            	radar_server_data.get('primary'),
		'is_server_aggregate':          	radar_server_data.get('aggregate'),
		'is_server_locked':             	radar_server_data.get('locked'),
		'is_radar_network_up':          	radar_server_data.get('radarNetworkUp'),
		'collection_time':              	parse_timestamp(radar_server_data
																.get('collectionTime')),
		'reporting_host':               	radar_server_data.get('reportingHost'),
		'last_ping_at':                 	(parse_timestamp(radar_server_data
																.get('ping', {})
																.get('timestamp'))),
		'ping_responses_ldm':           	(radar_server_data.get('ping', {})
															  .get('targets', {})
															  .get('ldm')),
		'ping_responses_radar':         	(radar_server_data.get('ping', {})
															  .get('targets', {})
															  .get('radar')),
		'ping_responses_server':        	(radar_server_data.get('ping', {})
															  .get('targets', {})
															  .get('server')),
		'ping_responses_network':          	(radar_server_data.get('ping', {})
															  .get('targets', {})
															  .get('misc')),
		'network_interfaces_refreshed_at':	(parse_timestamp(radar_server_data
																.get('network', {})
																.get('timestamp'))),
		'interfaces':                   	[],
	}
	server = RadarServer(**server_dict)
	for item in radar_server_data.get('network', {}):
		if item != 'timestamp':
			interface_dict = {
				'interface_name':       (radar_server_data.get('network', {})
														  .get(item, {})
														  .get('interface')),
				'is_interface_active':  (radar_server_data.get('network', {})
														  .get(item, {})
														  .get('active')),
				'packets_out_ok':       (radar_server_data.get('network', {})
														  .get(item, {})
														  .get('transNoError')),
				'packets_out_error':    (radar_server_data.get('network', {})
														  .get(item, {})
														  .get('transError')),
				'packets_out_dropped':  (radar_server_data.get('network', {})
														  .get(item, {})
														  .get('transDropped')),
				'packets_out_overrun':  (radar_server_data.get('network', {})
														  .get(item, {})
														  .get('transOverrun')),
				'packets_in_ok':        (radar_server_data.get('network', {})
														  .get(item, {})
														  .get('recvNoError')),
				'packets_in_error':     (radar_server_data.get('network', {})
														  .get(item, {})
														  .get('recvError')),
				'packets_in_dropped':   (radar_server_data.get('network', {})
														  .get(item, {})
														  .get('recvDropped')),
				'packets_in_overrun':   (radar_server_data.get('network', {})
														  .get(item, {})
														  .get('recvOverrun')),
			}
			server.interfaces.append(NetworkInterface(**interface_dict))
	return server


@display_spinner('Getting radar station alarms...')
def get_radar_station_alarms(
	session: CachedSession,
	radar_station_id: str
) -> List[RadarStationAlarm]:
	""" """
	radar_alarm_data = api_request(session, (NWS_API_RADAR_STATIONS
											 + radar_station_id
											 + '/alarms'))
	response = radar_alarm_data.get('response')
	retrieved_at = radar_alarm_data.get('retrieved_at')
	radar_alarms = []
	for alarm in response.get('@graph', {}):
		alarm_dict = {
			'retrieved_at':	retrieved_at,
			'status':				alarm.get('status'),
			'message':				alarm.get('message'),
			'event_at':				alarm.get('timestamp'),
			'active_channel':		alarm.get('activeChannel'),
		}
		radar_alarms.append(RadarStationAlarm(**alarm_dict))
	return radar_alarms


@display_spinner('Getting radar stations...')
def get_radar_stations(session: CachedSession) -> List[RadarStation]:
	""" """
	radar_stations_data = api_request(session, NWS_API_RADAR_STATIONS)
	response = radar_stations_data.get('response')
	retrieved_at = radar_stations_data.get('retrieved_at')
	stations = []
	for feature in response.get('features', {}):
		stations.append(process_radar_station_data(feature, retrieved_at))
	return stations


@display_spinner('Getting radar station details...')
def get_radar_station(
	session: CachedSession,
	station_id: str
) -> RadarStation:
	""" """
	radar_station_data = api_request(session, NWS_API_RADAR_STATIONS + station_id)
	response = radar_station_data.get('response')
	retrieved_at = radar_station_data.get('retrieved_at')
	return process_radar_station_data(response, retrieved_at)


# See:
# - https://www.ncdc.noaa.gov/wct/data.php
#
# LDM = Local Data Manager
# RDS = Remote Data Server
# TDS = THREDDs Data Server
#
# NOTE: The official API documentation doesn't include a schema for the radar
# servers and stations endpoints, so some field meanings are inferred from the data.
@display_spinner('Getting radar servers...')
def get_radar_servers(session: CachedSession) -> List[RadarServer]:
	""" """
	radar_servers_data = api_request(session, NWS_API_RADAR_SERVERS)
	response = radar_servers_data.get('response')
	retrieved_at = radar_servers_data.get('retrieved_at')
	servers = []
	for feature in response.get('@graph', {}):
		servers.append(process_radar_server_data(feature, retrieved_at))
	return servers


@display_spinner('Getting radar server details...')
def get_radar_server(
	session: CachedSession,
	server_id: str
) -> RadarServer:
	""" """
	radar_server_data = api_request(session, NWS_API_RADAR_SERVERS + server_id)
	response = radar_server_data.get('response')
	retrieved_at = radar_server_data.get('retrieved_at')
	return process_radar_server_data(response, retrieved_at)


@display_spinner('Getting radar queue for host and station...')
def get_radar_queue(
	session: CachedSession,
	ldm_host: str,
	station_id: str
) -> List[RadarQueueItem]:
	""" """
	radar_queue_data = api_request(session, (NWS_API_RADAR_QUEUES
											 + ldm_host
											 + f'?station={station_id}'))
	response = radar_queue_data.get('response')
	retrieved_at = radar_queue_data.get('retrieved_at')
	radar_queue = []
	for item in response.get('@graph', {}):
		radar_queue_dict = {
			'retrieved_at':	retrieved_at,
			'radar_station_id':		station_id,
			'host':					item.get('host'),
			'arrived_at':			item.get('arrivalTime'),
			'created_at':			item.get('createdAt'),
			'station_id':			item.get('stationId'),
			'queue_item_type':		item.get('type'),
			'feed':					item.get('feed'),
			'resolution_version':	item.get('resolutionVersion'),
			'sequence_number':		item.get('sequenceNumber'),
			'size':					item.get('size'),
		}
		radar_queue.append(RadarQueueItem(**radar_queue_dict))
	return radar_queue