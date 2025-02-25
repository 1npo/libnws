from requests_cache import CachedSession
from libnws.render.decorators import display_spinner
from libnws.api.api_request import api_request
from libnws.api import NWS_API_GLOSSARY


@display_spinner('Getting glossary...')
def get_glossary(session: CachedSession) -> dict:
	"""Get the glossary of weather terms"""
	glossary_data = api_request(session, NWS_API_GLOSSARY)
	response = glossary_data.get('response')
	glossary = {}
	for entry in response.get('glossary', {}):
		term = entry.get('term')
		definition = entry.get('definition')
		if term and definition:
			glossary.update({term: definition})
	return glossary
