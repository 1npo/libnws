from typing import List, Dict
from datetime import datetime
from dataclasses import dataclass
from libnws.model.nws_item import NWSItem


# See: https://www.ncei.noaa.gov/products/radar/next-generation-weather-radar
@dataclass(kw_only=True)
class RadarDataAcquisition(NWSItem):
    refreshed_at: str
    reporting_host: str
    mode: str
    status: str
    control_status: str
    operability_status: str
    super_resolution_status: str
    generator_state: str
    alarm_summary: str
    resolution_version: str
    nexrad_l2_path: str
    volume_coverage_pattern: str
    build_number: float
    average_tx_power_w: float
    reflectivity_calibration_correction_db: float


@dataclass(kw_only=True)
class RadarPerformance(NWSItem):
    refreshed_at: datetime
    performance_checked_at: datetime
    reporting_host: str
    ntp_status: int
    command_channel: str
    linearity: float
    power_source: str
    fuel_level_pc: float
    dynamic_range_db: float
    transmitter_peak_power_kw: float
    transmitter_recycle_count: int
    transmitter_imbalance_db: float
    transmitter_leaving_air_temp_c: float
    transmitter_leaving_air_temp_f: float
    shelter_temp_c: float
    shelter_temp_f: float
    radome_air_temp_c: float
    radome_air_temp_f: float
    horizontal_noise_temp_c: float
    horizontal_noise_temp_f: float
    transitional_power_source: str
    elevation_encoder_light: str
    azimuth_encoder_light: str
    horizontal_delta_db: float
    vertical_delta_db: float
    receiver_bias_db: float
    horizontal_short_pulse_noise_db_m: float
    horizontal_short_pulse_noise_db_mi: float
    horizontal_long_pulse_noise_db_m: float
    horizontal_long_pulse_noise_db_mi: float


@dataclass(kw_only=True)
class RadarPathLoss(NWSItem):
    wg04_circulator: float
    wg02_harmonic_filter: float
    wg06_spectrum_filter: float
    ifd_rif_anti_alias_filter: float
    ifd_burst_anti_alias_filter: float
    a6_arc_detector: float
    transmitter_coupler_coupling: float
    vertical_f_heliax_to_4at16: float
    horizontal_f_heliax_to_4at17: float
    at4_attenuator: float
    waveguide_klystron_to_switch: float


@dataclass(kw_only=True)
class RadarAdaptation(NWSItem):
    refreshed_at: datetime
    reporting_host: str
    transmitter_frequency: int
    transmitter_power_data_watts_factor: float
    antenna_gain_incl_radome: float
    coho_power_at_a1j4: float
    stalo_power_at_a1j2: float
    horizontal_receiver_noise_long_pulse: float
    horizontal_receiver_noise_short_pulse: float
    transmitter_spectrum_filter_installed: str # bool? are "F" and "T" the only values?
    pulse_width_transmitter_out_long_pulse: int
    pulse_width_transmitter_out_short_pulse: int
    ame_noise_source_horizontal_excess_noise_ratio: float
    ame_horizontal_test_signal_power: float
    path_loss: RadarPathLoss


@dataclass(kw_only=True)
class RadarStationAlarm(NWSItem):
    retrieved_at: datetime
    status: str
    message: str
    active_channel: int
    event_at: datetime


@dataclass(kw_only=True)
class RadarQueueItem(NWSItem):
    retrieved_at: datetime
    radar_station_id: str
    host: str
    arrived_at: datetime
    created_at: datetime
    station_id: str
    queue_item_type: str
    feed: str
    resolution_version: int
    sequence_number: str
    size: int


@dataclass(kw_only=True)
class RadarStation(NWSItem):
    retrieved_at: datetime
    radar_station_id: str
    name: str
    station_type: str
    timezone: str
    lat: float
    lon: float
    server_host: str
    reporting_host: str
    elevation_m: float
    elevation_mi: float 
    latency_current_s: float
    latency_average_s: float
    latency_max_s: float
    latency_nexrad_l2_last_received_at: datetime
    max_latency_at: datetime
    radar_data_acquisition: RadarDataAcquisition
    performance: RadarPerformance
    adaptation: RadarAdaptation


@dataclass(kw_only=True)
class NetworkInterface(NWSItem):
    interface_name: str
    is_interface_active: bool
    packets_out_ok: int
    packets_out_error: int
    packets_out_dropped: int
    packets_out_overrun: int
    packets_in_ok: int
    packets_in_error: int
    packets_in_dropped: int
    packets_in_overrun: int


@dataclass(kw_only=True)
class RadarServer(NWSItem):
    retrieved_at: datetime
    host: str
    server_type: str
    up_since: datetime
    hardware_refreshed_at: datetime
    network_interfaces_refreshed_at: datetime
    cpu: float
    memory: float
    io_utilization: float
    disk: int
    load_1: float
    load_5: float
    load_15: float
    interfaces: List[NetworkInterface]
    command_last_executed: str
    command_last_executed_at: datetime
    command_last_nexrad_data_at: datetime
    command_last_received: str
    command_last_received_at: datetime
    command_last_refreshed_at: datetime
    ldm_refreshed_at: datetime
    ldm_latest_product_at: datetime
    ldm_oldest_product_at: datetime
    ldm_storage_size: int
    ldm_count: int
    is_ldm_active: bool
    is_server_active: bool
    is_server_primary: bool
    is_server_aggregate: bool
    is_server_locked: bool
    is_radar_network_up: bool
    collection_time: datetime
    reporting_host: str
    last_ping_at: datetime
    ping_responses_ldm: Dict[str, bool]
    ping_responses_radar: Dict[str, bool]
    ping_responses_server: Dict[str, bool]
    ping_responses_network: Dict[str, bool]
    
