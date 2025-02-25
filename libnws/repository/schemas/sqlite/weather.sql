----------
-- WEATHER
----------

CREATE TABLE IF NOT EXISTS observations
(
    retrieved_at                TEXT, -- ISO8601 timestamp
    station_or_zone_id          TEXT,
    observed_at	                TEXT, -- ISO8601 timestamp
    icon_url	                TEXT,
    text_description	        TEXT,
    raw_message	                TEXT,
    station_elevation_m	        INTEGER,
    station_elevation_mi	    REAL,
    temperature_c	            REAL,
    temperature_f	            REAL,
    dew_point_c	                REAL,
    dew_point_f	                REAL,
    wind_direction_deg_ang	    INTEGER,
    wind_direction_compass	    TEXT,
    wind_speed_kmh	            REAL,
    wind_speed_mph	            REAL,
    wind_gust_kmh	            REAL,
    wind_gust_mph	            REAL,
    barometric_pressure_pa	    INTEGER,
    barometric_pressure_inhg	REAL,
    sea_level_pressure_pa	    INTEGER,
    sea_level_pressure_inhg	    REAL,
    visibility_m	            INTEGER,
    visibility_mi	            REAL,
    max_temp_last_24h_c	        REAL,
    max_temp_last_24h_f	        REAL,
    min_temp_last_24h_c	        REAL,
    min_temp_last_24h_f	        REAL,
    precip_last_1h_mm	        REAL,
    precip_last_3h_mm	        REAL,
    precip_last_6h_mm	        REAL,
    relative_humidity_pc	    REAL,
    wind_chill_c	            REAL,
    wind_chill_f	            REAL,
    heat_index_c	            REAL,
    heat_index_f	            REAL,
    PRIMARY KEY                 (retrieved_at, station_or_zone_id)
);

CREATE TABLE IF NOT EXISTS observations_cloud_layers
(
    retrieved_at            TEXT, -- ISO8601 timestamp
    station_or_zone_id      TEXT,
    cloud_layer_height	    TEXT,
    cloud_layer_description	TEXT,
    PRIMARY KEY             (retrieved_at, station_or_zone_id, cloud_layer_height),
    FOREIGN KEY             (retrieved_at, station_or_zone_id) REFERENCES observations (retrieved_at, station_or_zone_id)
);

CREATE TABLE IF NOT EXISTS forecasts
(
    retrieved_at                    TEXT, -- ISO8601 timestamp
    forecast_office                 TEXT,
    grid_x                          INTEGER,
    grid_y                          INTEGER,
    generated_at	                TEXT, -- ISO8601 timestamp
    updated_at	                    TEXT, -- ISO8601 timestamp
    period_num	                    INTEGER,
    period_name	                    TEXT,
    start_at	                    TEXT, -- ISO8601 timestamp
    end_at	                        TEXT, -- ISO8601 timestamp
    forecast_short	                TEXT,
    forecast_detailed	            TEXT,
    forecast_icon_url	            TEXT,
    is_daytime	                    INTEGER, -- boolean
    wind_speed	                    TEXT,
    wind_direction	                TEXT,
    temperature_trend	            TEXT,
    temperature_c	                REAL,
    temperature_f	                REAL,
    dew_point_c	                    REAL,
    dew_point_f	                    REAL,
    relative_humidity_pc	        REAL,
    precipitation_probability_pc    REAL,
    PRIMARY KEY                     (retrieved_at, forecast_office, grid_x, grid_y)
);
