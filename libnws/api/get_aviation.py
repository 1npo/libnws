import json
from typing import List
from datetime import datetime
from requests_cache import CachedSession
from libnws.render.decorators import display_spinner
from libnws.api.api_request import api_request
from libnws.api import (
    NWS_API_AVIATION_SIGMETS,
    NWS_API_AVIATION_CWSU,
)
from libnws.model.aviation import SIGMET, CenterWeatherAdvisory, CentralWeatherServiceUnit


def process_sigmet_data(sigmet_data: dict, retrieved_at: datetime) -> SIGMET:
    sigmet_dict = {
        'retrieved_at': retrieved_at,
        'url':          sigmet_data.get('properties', {}).get('id'),
        'issued_at':    sigmet_data.get('properties', {}).get('issueTime'),
        'effective_at': sigmet_data.get('properties', {}).get('start'),
        'expires_at':   sigmet_data.get('properties', {}).get('end'),
        'fir':          sigmet_data.get('properties', {}).get('fir'),
        'atsu':         sigmet_data.get('properties', {}).get('atsu'),
        'sequence':     sigmet_data.get('properties', {}).get('sequence'),
        'phenomenon':   sigmet_data.get('properties', {}).get('phenomenon'),
        'area_polygon': None,
    }
    geometry = sigmet_data.get('geometry')
    if geometry:
        geometry_json = json.dumps({'coordinates': geometry.get('coordinates')})
        sigmet_dict.update({'area_polygon': geometry_json})
    return SIGMET(**sigmet_dict)


def process_sigmets(sigmets_data: list, retrieved_at: datetime) -> List[SIGMET]:
    sigmets = []
    for feature in sigmets_data.get('features', {}):
        sigmets.append(process_sigmet_data(feature, retrieved_at))
    return sigmets


@display_spinner('Getting all SIGMETs...')
def get_all_sigmets(session: CachedSession) -> List[SIGMET]:
    sigmets_data = api_request(session, NWS_API_AVIATION_SIGMETS)
    response = sigmets_data.get('response')
    retrieved_at = sigmets_data.get('retrieved_at')
    return process_sigmets(response, retrieved_at)


@display_spinner('Getting all SIGMETs issued by ATSU...')
def get_all_atsu_sigmets(
    session: CachedSession,
    atsu: str
) -> List[SIGMET]:
    sigmets_data = api_request(session, NWS_API_AVIATION_SIGMETS + atsu)
    response = sigmets_data.get('response')
    retrieved_at = sigmets_data.get('retrieved_at')
    return process_sigmets(response, retrieved_at)


@display_spinner('Getting all SIGMETs issued by ATSU on date...')
def get_all_atsu_sigmets_by_date(
    session: CachedSession,
    atsu: str,
    date_str: str
) -> List[SIGMET]:
    sigmets_data = api_request(session, NWS_API_AVIATION_SIGMETS + atsu + f'/{date_str}')
    response = sigmets_data.get('response')
    retrieved_at = sigmets_data.get('retrieved_at')
    return process_sigmets(response, retrieved_at)


@display_spinner('Getting SIGMET...')
def get_sigmet(
    session: CachedSession,
    atsu: str,
    date_str: str,
    time_str
) -> SIGMET:
    sigmet_data = api_request(session, (NWS_API_AVIATION_SIGMETS
                                        + atsu
                                        + f'/{date_str}/{time_str}'))
    response = sigmet_data.get('response')
    retrieved_at = sigmet_data.get('retrieved_at')
    return process_sigmets(response, retrieved_at)


def process_cwa_data(cwa_data: dict, retrieved_at: datetime) -> CenterWeatherAdvisory:
    cwa_dict = {
        'retrieved_at':             retrieved_at,
        'url':                      cwa_data.get('properties', {}).get('id'),
        'text':                     cwa_data.get('properties', {}).get('text'),
        'cwsu':                     cwa_data.get('properties', {}).get('cwsu'),
        'sequence':                 cwa_data.get('properties', {}).get('sequence'),
        'issued_at':                cwa_data.get('properties', {}).get('issueTime'),
        'effective_at':             cwa_data.get('properties', {}).get('start'),
        'expires_at':               cwa_data.get('properties', {}).get('end'),
        'observed_property_url':    (cwa_data.get('properties', {})
                                             .get('observedProperty')),
        'area_polygon':             None,
    }
    geometry = cwa_data.get('geometry')
    if geometry:
        cwa_dict.update({'area_polygon': geometry.get('coordinates')})
    return CenterWeatherAdvisory(**cwa_dict)


@display_spinner('Getting CWSU details...')
def get_cwsu(
    session: CachedSession,
    cwsu_id: str
) -> CentralWeatherServiceUnit:
    cwsu_data = api_request(session, NWS_API_AVIATION_CWSU + cwsu_id)
    response = cwsu_data.get('response')
    retrieved_at = cwsu_data.get('retrieved_at')
    cwsu_dict = {
        'retrieved_at':         retrieved_at,
        'cwsu_id':              response.get('id'),
        'street':               response.get('street'),
        'name':                 response.get('name'),
        'city':                 response.get('city'),
        'state':                response.get('state'),
        'zip_code':             response.get('zipCcode'),
        'email':                response.get('email'),
        'fax':                  response.get('fax'),
        'phone':                response.get('phone'),
        'url':                  response.get('url'),
        'nws_region':           response.get('nwsRegion'),
    }
    return CentralWeatherServiceUnit(**cwsu_dict)


@display_spinner('Getting all CWAs issued by CWSU...')
def get_cwas(
    session: CachedSession,
    cwsu_id: str
) -> List[CenterWeatherAdvisory]:
    cwas_data = api_request(session, NWS_API_AVIATION_CWSU + cwsu_id + '/cwas')
    response = cwas_data.get('response')
    retrieved_at = cwas_data.get('retrieved_at')
    cwas = []
    for feature in response.get('features', {}):
        cwas.append(process_cwa_data(feature, retrieved_at))
    return cwas


@display_spinner('Getting CWA...')
def get_cwa(
    session: CachedSession,
    cwsu_id: str,
    date_str: str,
    sequence: int
) -> CenterWeatherAdvisory:
    cwa_data = api_request(session, (NWS_API_AVIATION_CWSU
                                     + cwsu_id
                                     + f'/cwas/{date_str}/{sequence}'))
    response = cwa_data.get('response')
    retrieved_at = cwa_data.get('retrieved_at')
    return process_cwa_data(response, retrieved_at)
