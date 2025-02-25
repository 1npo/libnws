import pytz
from datetime import datetime
from requests_cache import CachedSession


def api_request(
	session: CachedSession,
	url: str
) -> dict:
	response = session.get(url)
	data = response.json()
	created_at = response.created_at
	return {'response': data, 'retrieved_at': created_at}


def parse_timestamp(timestamp: str) -> datetime | None:
	if timestamp:
		return (
			datetime.fromisoformat(timestamp)
					.astimezone(pytz.timezone('US/Eastern'))
					.replace(tzinfo=None)
		)
