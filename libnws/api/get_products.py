from typing import List
from datetime import datetime
from requests_cache import CachedSession
from libnws.render.decorators import display_spinner
from libnws.api.api_request import api_request
from libnws.api import (
	NWS_API_PRODUCT_TYPES,
	NWS_API_PRODUCT_LOCATIONS,
	NWS_API_PRODUCTS,
)
from libnws.model.products import Product, ProductLocation, ProductType


def process_product_data(products_data: dict, retrieved_at: datetime) -> List[Product]:
	products = []
	for product in products_data:
		product_dict = {
			'retrieved_at':	retrieved_at,
			'product_id':			product.get('id'),
			'wmo_id':				product.get('wmoCollectiveId'),
			'text':					None,
			'code':					product.get('productCode'),
			'name':					product.get('productName'),
			'issuing_office':		product.get('issuingOffice'),
			'issued_at':			product.get('issuanceTime'),
		}
		products.append(Product(**product_dict))
	return products


def process_product_types_data(product_types_data: list) -> List[ProductType]:
	product_types = []
	for product_type in product_types_data.get('@graph', {}):
		type_dict = {
			'code':	product_type.get('productCode'),
			'name': product_type.get('productName'),
		}
		product_types.append(ProductType(**type_dict))
	return product_types


def process_product_locations_data(product_locations_data: dict) -> List[ProductLocation]:
	product_locations = []
	product_locations_data = product_locations_data.get('locations', {})
	if product_locations_data and isinstance(product_locations_data, dict):
		for location, code in product_locations_data.items():
			location_dict = {
				'code': location,
				'name': code,
			}
			product_locations.append(ProductLocation(**location_dict))
		return product_locations
	return []


# See: https://www.weather.gov/mlb/text
@display_spinner('Getting all product types...')
def get_product_types(session: CachedSession) -> List[ProductType]:
	product_types_data = api_request(session, NWS_API_PRODUCT_TYPES).get('response')
	return process_product_types_data(product_types_data)


@display_spinner('Getting product types available from the issuing location...')
def get_product_types_by_location(
	session: CachedSession,
	location_id: str
) -> List[ProductType]:
	product_types_data = api_request(session, (NWS_API_PRODUCT_LOCATIONS
											   + f'/{location_id}/types').get('response'))
	return process_product_types_data(product_types_data)


@display_spinner('Getting all product issuing locations...')
def get_product_locations(session: CachedSession) -> List[ProductLocation]:
	product_locations_data = api_request(session,
									  	 NWS_API_PRODUCT_LOCATIONS).get('response')
	return process_product_locations_data(product_locations_data)


@display_spinner('Getting product issuing locations by type...')
def get_product_locations_by_type(
	session: CachedSession,
	type_id: str
) -> List[ProductLocation]:
	product_locations_data = (
		api_request(session, (NWS_API_PRODUCT_TYPES
							  + f'/{type_id}/locations').get('response'))
	)
	return process_product_locations_data(product_locations_data)


@display_spinner('Getting listing of all products...')
def get_products(session: CachedSession) -> List[Product]:
	products_data = api_request(session, NWS_API_PRODUCTS)
	response = products_data.get('response')
	retrieved_at = products_data.get('retrieved_at')
	return process_product_data(response.get('@graph', {}), retrieved_at)


@display_spinner('Getting listing of all products by type...')
def get_products_by_type(
	session: CachedSession,
	type_id: str
) -> List[Product]:
	products_data = api_request(session, NWS_API_PRODUCT_TYPES + f'/{type_id}')
	response = products_data.get('response')
	retrieved_at = products_data.get('retrieved_at')
	return process_product_data(response.get('@graph', {}), retrieved_at)


@display_spinner('Getting listing of all products by type from the issuing location...')
def get_products_by_type_and_location(
	session: CachedSession, 
	type_id: str,
	location_id: str
) -> List[Product]:
	products_data = api_request(session, (NWS_API_PRODUCT_TYPES
										  + f'/{type_id}/locations/{location_id}'))
	response = products_data.get('response')
	retrieved_at = products_data.get('retrieved_at')
	return process_product_data(response.get('@graph', {}), retrieved_at)


@display_spinner('Getting product content...')
def get_product(
	session: CachedSession,
	product_id: str
) -> Product:
	""" """
	product_data = api_request(session, NWS_API_PRODUCTS + product_id)
	response = product_data.get('response')
	retrieved_at = product_data.get('retrieved_at')
	product = process_product_data([response], retrieved_at)[0]
	product.text = response.get('productText')
	return product

