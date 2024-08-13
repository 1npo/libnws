# See:
# - https://github.com/weather-gov/api/discussions/478
# - https://weather-gov.github.io/api/general-faqs, especially these sections:
#   - "How do I get a forecast for a location from the API?"
#   - "How do I know I'm getting the latest data? Do I need to use “cache busting” methods?"
API_URL_USCB_GEOCODE = 'https://geocoding.geo.census.gov/geocoder/locations/onelineaddress?benchmark=Public_AR_Current&format=json&address='
API_URL_NWS_POINTS = 'https://api.weather.gov/points/'
API_URL_NWS_STATIONS = 'https://api.weather.gov/stations/'
API_URL_NWS_ALERTS_AREA = 'http://api.weather.gov/alerts/active/area/'
API_URL_NWS_GLOSSARY = 'https://api.weather.gov/glossary'
API_URL_NWS_SERVERS = 'http://api.weather.gov/radar/servers'
API_URL_NWS_RADERS = 'http://api.weather.gov/radar/radars'

# See: https://codes.wmo.int/common/unit
WMI_UNIT_MAP = {                            
    'wmoUnit:Pa':               'pa',       # pressure in pascals
    'wmoUnit:km_h-1':           'kmph',     # kilometers per hour
    'wmoUnit:m':                'm',        # meters
    'wmoUnit:percent':          'pc',       # percent
    'wmoUnit:mm':               'mm',       # milimeters
    'wmoUnit:degree_(angle)':   'deg_ang',  # degrees (angle)
    'wmoUnit:degC':             'c',        # degrees celsius
    'F':                        'f',        # degrees fahrenheit
}

# See:
# - https://www.atmos.albany.edu/facstaff/ralazear/ATM209/Home_files/METAR_Code.pdf
# - https://en.wikipedia.org/wiki/Okta
METAR_CLOUD_COVER_MAP = {
    'SKC':  'Clear Sky',
    'CLR':  'Clear Sky',
    'FEW':  'Few Clouds',           # 1-2 oktas (1/8 - 2/8 of sky covered)
    'SCT':  'Scattered Clouds',     # 3-4 oktas (3/8 - 4/8 of sky covered)
    'BKN':  'Broken Sky',           # 4-7 oktas (5/8 - 7/8 of sky covered)
    'OVC':  'Overcast',             # 8 oktas (sky completely covered)
}
