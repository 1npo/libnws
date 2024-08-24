"""
"""

from typing import List
from requests_cache import CachedSession
from nwsc.render.decorators import display_spinner
from nwsc.api.api_request import api_request, parse_timestamp
from nwsc.api import (
	NWS_API_ALERTS_AREA,
    NWS_API_ALERTS_ZONE,
    NWS_API_ALERTS_REGION,
    NWS_API_ALERTS,
    NWS_API_ALERT_TYPES,
    NWS_API_ALERT_COUNTS,
)
from nwsc.model.alerts import PriorAlert, Alert, AlertCounts


# See:
# - https://vlab.noaa.gov/web/nws-common-alerting-protocol
# - https://www.weather.gov/media/alert/CAP_v12_guide_05-16-2017.pdf
# - https://www.weather.gov/vtec/
def process_alert_data(alert_data: dict) -> List[Alert]:
	"""Get all current alerts for the given area, zone, or region"""
	alerts = []
	for feature in alert_data.get('features', {}):
		alert_dict = {
			'id':                   feature.get('properties', {}).get('id'),
			'url':                  feature.get('id'),
			'updated_at':           parse_timestamp(feature.get('updated')),
			'title':                feature.get('title'),
			'headline':            	feature.get('properties', {}).get('headline'),
			'description':         	feature.get('properties', {}).get('description'),
			'instruction':         	feature.get('properties', {}).get('instruction'),
			'urgency':             	feature.get('properties', {}).get('urgency'),
			'area_description':   	feature.get('properties', {}).get('areaDesc'),
			'affected_zones_urls':	feature.get('properties', {}).get('affectedZones'),
			'areas_ugc':            feature.get('properties', {}).get('geocode', {}).get('UGC'),
			'areas_same':           feature.get('properties', {}).get('geocode', {}).get('SAME'),
			'sent_by':             	feature.get('properties', {}).get('sender'),
			'sent_by_name':        	feature.get('properties', {}).get('senderName'),
			'sent_at':             	parse_timestamp(feature.get('properties', {}).get('sent')),
			'effective_at':        	parse_timestamp(feature.get('properties', {}).get('effective')),
			'ends_at':             	parse_timestamp(feature.get('properties', {}).get('ends')),
			'status':              	feature.get('properties', {}).get('status'),
			'message_type':        	feature.get('properties', {}).get('messageType'),
			'category':            	feature.get('properties', {}).get('category'),
			'certainty':           	feature.get('properties', {}).get('certainty'),
			'event_type':          	feature.get('properties', {}).get('event'),
			'onset_at':            	parse_timestamp(feature.get('properties', {}).get('onset')),
			'expires_at':          	parse_timestamp(feature.get('properties', {}).get('expires')),
			'response_type':       	feature.get('properties', {}).get('response'),
			'cap_awips_id':        	feature.get('properties', {}).get('parameters', {}).get('AWIPSidentifier'),
			'cap_wmo_id':          	feature.get('properties', {}).get('parameters', {}).get('WMOidentifier'),
			'cap_headline':        	feature.get('properties', {}).get('parameters', {}).get('NWSheadline'),
			'cap_blocked_channels':	feature.get('properties', {}).get('parameters', {}).get('BLOCKCHANNEL'),
			'cap_vtec':            	feature.get('properties', {}).get('parameters', {}).get('VTEC'),
			'prior_alerts':         [],
		}
		alert = Alert(**alert_dict)
		for reference in feature.get('properties', {}).get('references', {}):
			prior_alert_dict = {
				'id':           reference.get('identifier'),
				'url':          reference.get('@id'),
				'sent_at':      parse_timestamp(reference.get('sent')),
			}
			prior_alert = PriorAlert(**prior_alert_dict)
			alert.prior_alerts.append(prior_alert)
		alerts.append(alert)
	return alerts


@display_spinner('Getting all alerts...')
def get_alerts(session: CachedSession) -> List[Alert]:
	alerts = api_request(session, NWS_API_ALERTS)
	return process_alert_data(alerts)


@display_spinner('Getting alerts for the local area...')
def get_alerts_by_area(
	session: CachedSession,
	area: str
) -> List[Alert]:
	alerts = api_request(session, NWS_API_ALERTS_AREA + area)
	return process_alert_data(alerts)


@display_spinner('Getting alerts for zone...')
def get_alerts_by_zone(
	session: CachedSession,
	zone: str
) -> List[Alert]:
	alerts = api_request(session, NWS_API_ALERTS_ZONE + zone)
	return process_alert_data(alerts)


@display_spinner('Getting alerts for marine region...')
def get_alerts_by_region(
	session: CachedSession,
	region: str
) -> List[Alert]:
	alerts = api_request(session, NWS_API_ALERTS_REGION + region)
	return process_alert_data(alerts)


@display_spinner('Getting alerts for marine region...')
def get_alerts_by_id(
	session: CachedSession,
	alert_id: str
) -> List[Alert]:
	alerts = api_request(session, NWS_API_ALERTS + alert_id)
	return process_alert_data({'features': [alerts]})


@display_spinner('Getting alert types...')
def get_alert_types(session: CachedSession) -> List[Alert]:
	alert_types_data = api_request(session, NWS_API_ALERT_TYPES)
	return alert_types_data.get('eventTypes')


@display_spinner('Getting alert counts...')
def get_alert_counts(session: CachedSession) -> List[Alert]:
	alert_counts_data = api_request(session, NWS_API_ALERT_COUNTS)
	alert_counts_dict = {
		'total':	alert_counts_data.get('total'),
		'land':		alert_counts_data.get('land'),
		'marine':	alert_counts_data.get('marine'),
		'regions':	alert_counts_data.get('regions'),
		'areas':	alert_counts_data.get('areas'),
		'zones':	alert_counts_data.get('zones'),
	}
	alert_counts = AlertCounts(**alert_counts_dict)
	return alert_counts
