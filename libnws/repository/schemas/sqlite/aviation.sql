
-----------
-- AVIATION
-----------

CREATE TABLE IF NOT EXISTS sigmets
(
    retrieved_at    TEXT, -- ISO8601 timestamp
    issued_at	    TEXT, -- ISO8601 timestamp
    fir	            TEXT,
    atsu	        TEXT,
    sequence	    TEXT,
    url	            TEXT,
    effective_at	TEXT, -- ISO8601 timestamp
    expires_at	    TEXT, -- ISO8601 timestamp
    phenomenon	    TEXT,
    area_polygon    TEXT, -- GeoJSON polygon coordinate string
    PRIMARY KEY     (retrieved_at, issued_at, fir, atsu, sequence)
);

CREATE TABLE IF NOT EXISTS center_weather_advisories
(
    retrieved_at            TEXT, -- ISO8601 timestamp
    cwsu	                TEXT,
    sequence	            TEXT,
    issued_at	            TEXT, -- ISO8601 timestamp
    url	                    TEXT,
    text	                TEXT,
    effective_at	        TEXT, -- ISO8601 timestamp
    expires_at	            TEXT, -- ISO8601 timestamp
    observed_property_url	TEXT,
    area_polygon            TEXT, -- GeoJSON polygon coordinate string
    PRIMARY KEY             (retrieved_at, issued_at, cwsu, sequence)
);

CREATE TABLE IF NOT EXISTS central_weather_service_units
(
    cwsu_id	        TEXT,
    name	        TEXT,
    street	        TEXT,
    city	        TEXT,
    state	        TEXT,
    zip_code	    TEXT,
    email	        TEXT,
    fax	            TEXT,
    phone	        TEXT,
    url	            TEXT,
    nws_region	    TEXT,
    PRIMARY KEY     (cwsu_id)
);
