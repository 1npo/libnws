-----------
-- PRODUCTS
-----------

CREATE TABLE IF NOT EXISTS products
(
    retrieved_at    TEXT, -- ISO8601 timestamp
    product_id	    TEXT,
    wmo_id	        TEXT,
    name	        TEXT,
    code	        TEXT,
    text	        TEXT,
    issuing_office	TEXT,
    issued_at	    TEXT, -- ISO8601 timestamp
    PRIMARY KEY     (retrieved_at, product_id)
);

CREATE TABLE IF NOT EXISTS product_locations
(
    location_code	TEXT,
    location_name	TEXT,
    PRIMARY KEY     (location_code)
);

CREATE TABLE IF NOT EXISTS product_types
(
    type_code	TEXT,
    type_name	TEXT,
    PRIMARY KEY (type_code)
);
