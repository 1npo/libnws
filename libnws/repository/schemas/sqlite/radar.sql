---------
-- RADARS
---------

CREATE TABLE IF NOT EXISTS radar_stations
(
    retrieved_at                        TEXT, -- ISO8601 timestamp
    radar_station_id	                TEXT,
    name	                            TEXT,
    station_type	                    TEXT,
    timezone	                        TEXT,
    lat	                                REAL,
    lon	                                REAL,
    server_host	                        TEXT,
    reporting_host	                    TEXT,
    elevation_m	                        REAL,
    elevation_mi	                    REAL, 
    latency_current_s	                REAL,
    latency_average_s	                REAL,
    latency_max_s	                    REAL,
    latency_nexrad_l2_last_received_at	TEXT, -- ISO8601 timestamp
    max_latency_at	                    TEXT, -- ISO8601 timestamp
    PRIMARY KEY                         (retrieved_at, radar_station_id)
);

CREATE TABLE IF NOT EXISTS radar_adaptation
(
    retrieved_at                                    TEXT, -- ISO8601 timestamp
    radar_station_id                                TEXT,
    refreshed_at	                                TEXT, -- ISO8601 timestamp
    reporting_host	                                TEXT,
    transmitter_frequency	                        INTEGER,
    transmitter_power_data_watts_factor	            REAL,
    antenna_gain_incl_radome	                    REAL,
    coho_power_at_a1j4	                            REAL,
    stalo_power_at_a1j2	                            REAL,
    horizontal_receiver_noise_long_pulse	        REAL,
    horizontal_receiver_noise_short_pulse	        REAL,
    transmitter_spectrum_filter_installed	        TEXT, -- bool? are "F" and "T" the only values?
    pulse_width_transmitter_out_long_pulse	        INTEGER,
    pulse_width_transmitter_out_short_pulse	        INTEGER,
    ame_noise_source_horizontal_excess_noise_ratio	REAL,
    ame_horizontal_test_signal_power	            REAL,
    PRIMARY KEY                                     (retrieved_at, radar_station_id),
    FOREIGN KEY                                     (retrieved_at, radar_station_id) REFERENCES radar_stations (retrieved_at, radar_station_id)
);

CREATE TABLE IF NOT EXISTS radar_performance
(
    retrieved_at                        TEXT, -- ISO8601 timestamp
    radar_station_id                    TEXT,
    refreshed_at	                    TEXT, -- ISO8601 timestamp
    performance_checked_at	            TEXT, -- ISO8601 timestamp
    reporting_host	                    TEXT,
    ntp_status	                        INTEGER,
    command_channel	                    TEXT,
    linearity	                        REAL,
    power_source	                    TEXT,
    fuel_level_pc	                    REAL,
    dynamic_range_db	                REAL,
    transmitter_peak_power_kw	        REAL,
    transmitter_recycle_count	        INTEGER,
    transmitter_imbalance_db	        REAL,
    transmitter_leaving_air_temp_c	    REAL,
    transmitter_leaving_air_temp_f	    REAL,
    shelter_temp_c	                    REAL,
    shelter_temp_f	                    REAL,
    radome_air_temp_c	                REAL,
    radome_air_temp_f	                REAL,
    horizontal_noise_temp_c	            REAL,
    horizontal_noise_temp_f	            REAL,
    transitional_power_source	        TEXT,
    elevation_encoder_light	            TEXT,
    azimuth_encoder_light	            TEXT,
    horizontal_delta_db	                REAL,
    vertical_delta_db	                REAL,
    receiver_bias_db	                REAL,
    horizontal_short_pulse_noise_db_m	REAL,
    horizontal_short_pulse_noise_db_mi	REAL,
    horizontal_long_pulse_noise_db_m	REAL,
    horizontal_long_pulse_noise_db_mi	REAL,
    PRIMARY KEY                         (retrieved_at, radar_station_id),
    FOREIGN KEY                         (retrieved_at, radar_station_id) REFERENCES radar_stations (retrieved_at, radar_station_id)
);

CREATE TABLE IF NOT EXISTS radar_path_loss
(
    retrieved_at                    TEXT, -- ISO8601 timestamp
    radar_station_id                TEXT,
    wg04_circulator	                REAL,
    wg02_harmonic_filter	        REAL,
    wg06_spectrum_filter	        REAL,
    ifd_rif_anti_alias_filter	    REAL,
    ifd_burst_anti_alias_filter	    REAL,
    a6_arc_detector	                REAL,
    transmitter_coupler_coupling	REAL,
    vertical_f_heliax_to_4at16	    REAL,
    horizontal_f_heliax_to_4at17	REAL,
    at4_attenuator	                REAL,
    waveguide_klystron_to_switch	REAL,
    PRIMARY KEY                     (retrieved_at, radar_station_id),
    FOREIGN KEY                     (retrieved_at, radar_station_id) REFERENCES radar_stations (retrieved_at, radar_station_id)
);

CREATE TABLE IF NOT EXISTS radar_data_acquisition
(
    retrieved_at                            TEXT, -- ISO8601 timestamp
    radar_station_id                        TEXT,
    refreshed_at	                        TEXT, -- ISO8601 timestamp
    reporting_host	                        TEXT,
    mode	                                TEXT,
    status	                                TEXT,
    control_status	                        TEXT,
    operability_status	                    TEXT,
    super_resolution_status	                TEXT,
    generator_state	                        TEXT,
    alarm_summary	                        TEXT,
    resolution_version	                    TEXT,
    nexrad_l2_path	                        TEXT,
    volume_coverage_pattern	                TEXT,
    build_number	                        REAL,
    average_tx_power_w	                    REAL,
    reflectivity_calibration_correction_db	REAL,
    PRIMARY KEY                             (retrieved_at, radar_station_id),
    FOREIGN KEY                             (retrieved_at, radar_station_id) REFERENCES radar_stations (retrieved_at, radar_station_id)
);

----------------
-- RADAR SERVERS
----------------

CREATE TABLE IF NOT EXISTS radar_servers
(
    retrieved_at                    TEXT, -- ISO8601 timestamp
    host	                        TEXT,
    server_type	                    TEXT,
    up_since	                    TEXT, -- ISO8601 timestamp
    hardware_refreshed_at	        TEXT, -- ISO8601 timestamp
    network_interfaces_refreshed_at	TEXT, -- ISO8601 timestamp
    cpu	                            REAL,
    memory	                        REAL,
    io_utilization	                REAL,
    disk	                        INTEGER,
    load_1	                        REAL, 
    load_5	                        REAL, 
    load_15	                        REAL, 
    command_last_executed	        TEXT, 
    command_last_executed_at	    TEXT, -- ISO8601 timestamp
    command_last_nexrad_data_at	    TEXT, -- ISO8601 timestamp
    command_last_received	        TEXT, 
    command_last_received_at	    TEXT, -- ISO8601 timestamp
    command_last_refreshed_at	    TEXT, -- ISO8601 timestamp
    ldm_refreshed_at	            TEXT, -- ISO8601 timestamp
    ldm_latest_product_at	        TEXT, -- ISO8601 timestamp
    ldm_oldest_product_at	        TEXT, -- ISO8601 timestamp
    ldm_storage_size	            INTEGER,
    ldm_count	                    INTEGER,
    is_ldm_active	                INTEGER, -- boolean
    is_server_active	            INTEGER, -- boolean
    is_server_primary	            INTEGER, -- boolean
    is_server_aggregate	            INTEGER, -- boolean
    is_server_locked	            INTEGER, -- boolean
    is_radar_network_up	            INTEGER, -- boolean
    collection_time	                TEXT, -- ISO8601 timestamp
    reporting_host	                TEXT,
    last_ping_at	                TEXT, -- ISO8601 timestamp
    PRIMARY KEY                     (retrieved_at, host)
);

CREATE TABLE IF NOT EXISTS rader_server_ping_responses
(
    retrieved_at        TEXT, -- ISO8601 timestamp
    host                TEXT,   
    ldm_name	        TEXT,
    ldm_response	    INTEGER, -- boolean
    radar_name	        TEXT,
    radar_response	    INTEGER, -- boolean
    server_name	        TEXT,
    server_response	    INTEGER, -- boolean
    network_name	    TEXT,
    network_response	INTEGER, -- boolean
    PRIMARY KEY         (retrieved_at, host),
    FOREIGN KEY         (retrieved_at, host) REFERENCES radar_servers (retrieved_at, host)
);

CREATE TABLE IF NOT EXISTS network_interfaces
(
    retrieved_at        TEXT, -- ISO8601 timestamp
    host                TEXT,   
    interface_name	    TEXT,
    is_interface_active	INTEGER, -- boolean
    packets_out_ok	    INTEGER,
    packets_out_error	INTEGER,
    packets_out_dropped	INTEGER,
    packets_out_overrun	INTEGER,
    packets_in_ok	    INTEGER,
    packets_in_error	INTEGER,
    packets_in_dropped	INTEGER,
    packets_in_overrun	INTEGER,
    PRIMARY KEY         (retrieved_at, host),
    FOREIGN KEY         (retrieved_at, host) REFERENCES radar_servers (retrieved_at, host)
);

---------------
-- RADAR QUEUES
---------------

CREATE TABLE IF NOT EXISTS radar_queues
(
    retrieved_at        TEXT, -- ISO8601 timestamp
    host	            TEXT,
    station_id	        TEXT,
    arrived_at	        TEXT, -- ISO8601 timestamp
    created_at	        TEXT, -- ISO8601 timestamp
    queue_item_type	    TEXT,
    feed	            TEXT,
    resolution_version	INTEGER,
    sequence_number	    TEXT,
    size	            INTEGER,
    PRIMARY KEY         (retrieved_at, host, station_id)   
);

---------------
-- RADAR ALARMS
---------------

CREATE TABLE IF NOT EXISTS radar_station_alarms
(
    event_at	    TEXT, -- ISO8601 timestamp
    status	        TEXT,
    message	        TEXT,
    active_channel	INTEGER,
    PRIMARY KEY     (event_at)
);
