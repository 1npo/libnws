from typing import List
from datetime import datetime
from requests_cache import CachedSession
from nwsc.render.decorators import display_spinner
from nwsc.api.api_request import api_request
from nwsc.api import (
    NWS_API_OFFICES,
    VALID_NWS_FORECAST_OFFICES,
)
from nwsc.model.offices import Office, OfficeHeadline


InvalidOfficeException = ValueError(
    f'Invalid forecast office. Please specify a valid forecast office: '
    f'{", ".join(VALID_NWS_FORECAST_OFFICES)}'
)


def process_headline_data(headline_data: dict, response_timestamp: datetime) -> dict:
    headline_dict = {
        'response_timestamp':   response_timestamp,
        'headline_id':          headline_data.get('id'),
        'name':                 headline_data.get('name'),
        'title':                headline_data.get('title'),
        'issued_at':            headline_data.get('issuanceTime'),
        'url':                  headline_data.get('link'),
        'content':              headline_data.get('content'),
        'headline_summary':     headline_data.get('summary'),
        'office_url':           headline_data.get('office'),
        'is_important':         headline_data.get('important'),
    }
    return OfficeHeadline(**headline_dict)


@display_spinner('Getting office headlines...')
def get_office_headlines(
    session: CachedSession,
    office_id: str
) -> List[OfficeHeadline]:
    if office_id not in VALID_NWS_FORECAST_OFFICES:
        raise InvalidOfficeException
    headlines_data = api_request(session, NWS_API_OFFICES + office_id + '/headlines')
    response = headlines_data.get('response')
    response_timestamp = headlines_data.get('response_timestamp')
    headlines = []
    for headline in response.get('@graph', {}):
        headlines.append(process_headline_data(headline, response_timestamp))
    return headlines


@display_spinner('Getting headline from office...')
def get_office_headline(
    session: CachedSession,
    office_id: str,
    headline_id: str
) -> OfficeHeadline:
    if office_id not in VALID_NWS_FORECAST_OFFICES:
        raise InvalidOfficeException
    headline_data = api_request(session, NWS_API_OFFICES + office_id + '/headlines/' + headline_id)
    response = headline_data.get('response')
    response_timestamp = headline_data.get('response_timestamp')
    return process_headline_data(response, response_timestamp)


@display_spinner('Getting forecast office details...')
def get_office(
    session: CachedSession,
    office_id: str
) -> Office:
    if office_id not in VALID_NWS_FORECAST_OFFICES:
        raise InvalidOfficeException
    office_data = api_request(session, NWS_API_OFFICES + office_id)
    response = office_data.get('response')
    response_timestamp = office_data.get('response_timestamp')
    office_dict = {
        'response_timestamp':   response_timestamp,
        'office_id':            office_data.get('id'),
        'name':                 office_data.get('name'),
        'street_address':       office_data.get('address', {}).get('streetAddress'),
        'city':                 office_data.get('address', {}).get('addressLocality'),
        'state':                office_data.get('address', {}).get('addressRegion'),
        'zip_code':             office_data.get('address', {}).get('postalCode'),
        'phone_number':         office_data.get('telephone'),
        'fax_number':           office_data.get('faxNumber'),
        'email':                office_data.get('email'),
        'url':                  office_data.get('sameAs'),
        'parent_url':           office_data.get('parentOrganization'),
        'nws_region':           office_data.get('nwsRegion'),
        'counties':             office_data.get('responsibleCounties'),
        'forecast_zones':       office_data.get('responsibleForecastZones'),
        'fire_zones':           office_data.get('responsibleFireZones'),
        'observation_stations': office_data.get('approvedObservationStations'),
    }
    return Office(**office_dict)
