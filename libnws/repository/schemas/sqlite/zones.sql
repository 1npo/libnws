--------
-- ZONES
--------

CREATE TABLE IF NOT EXISTS zones
(
    zone_id	        TEXT,
    grid_id	        TEXT,
    awips_id	    TEXT,
    name	        TEXT,
    zone_type	    TEXT,
    state	        TEXT,
    url	            TEXT,
    effective_at	TEXT, -- ISO8601 timestamp
    expires_at	    TEXT, -- ISO8601 timestamp
    multi_polygon   TEXT, -- GeoJSON multi-polygon coordinate string
    PRIMARY KEY     (zone_id)
);

CREATE TABLE IF NOT EXISTS zone_county_warning_areas
(
    zone_id	            TEXT,
    county_warning_area	TEXT,
    PRIMARY KEY         (zone_id, county_warning_area),
    FOREIGN KEY         (zone_id) REFERENCES zones (zone_id)
);

CREATE TABLE IF NOT EXISTS zone_observation_stations
(
    zone_id	            TEXT,
    observation_station	TEXT,
    PRIMARY KEY         (zone_id, observation_station),
    FOREIGN KEY         (zone_id) REFERENCES zones (zone_id)
);

CREATE TABLE IF NOT EXISTS zone_forecast_offices
(
    zone_id	        TEXT,
    forecast_office	TEXT,
    PRIMARY KEY     (zone_id, forecast_office),
    FOREIGN KEY     (zone_id) REFERENCES zones (zone_id)
);

CREATE TABLE IF NOT EXISTS zone_timezones
(
    zone_id	    TEXT,
    timezone	TEXT,
    PRIMARY KEY (zone_id, timezone),
    FOREIGN KEY (zone_id) REFERENCES zones (zone_id)
);

CREATE TABLE IF NOT EXISTS zone_forecast
(
    zone_id             TEXT,
    forecasted_at	    TEXT, -- ISO8601 timestamp
    period_num	        INTEGER,
    period_name	        TEXT,
    forecast_detailed	TEXT,
    PRIMARY KEY         (zone_id, forecasted_at, period_num),
    FOREIGN KEY         (zone_id) REFERENCES zones (zone_id)
);
