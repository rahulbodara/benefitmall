from django.core.management.base import BaseCommand
from django.core.cache import cache
from django.utils.text import slugify
from django.conf import settings
import requests
import logging
logger = logging.getLogger(__name__)

PRODUCT_ORDER = {
	'Medical': 1,
	'Dental': 2,
	'Vision': 3,
	'Life': 4,
	'Disability': 5,
}
INSURANCE_TYPE_ORDER = {
	'Small Group': 1,
	'Large Group': 2,
	'Self-Funded': 3,
	'Individual': 4,
	'Senior': 5,
}


class Command(BaseCommand):
	def handle(self, *args, **options):
		try:
			cachekey = 'carriers'

			params = {
				'grant_type': 'password',
				'client_id': settings.CARRIER_API_CLIENT_ID,
				'client_secret': settings.CARRIER_API_CLIENT_SECRET,
				'username': settings.CARRIER_API_USER,
				'password': settings.CARRIER_API_PASS + settings.CARRIER_API_TOKEN,
			}

			r = requests.post(settings.CARRIER_API_URL + settings.CARRIER_API_AUTH_URL, params=params)
			access_token = r.json().get("access_token")
			instance_url = r.json().get("instance_url")

			headers = {
				'Content-type': 'application/json',
				'Accept-Encoding': 'gzip',
				'Authorization': 'Bearer %s' % access_token
			}

			r = requests.request('get', settings.CARRIER_API_URL + settings.CARRIER_API_ENDPOINT, headers=headers, params=params,)
			ret = r.json()
			carriers = {}
			for item in ret:
				# "Carrier_Id": "001g000002ETUdlAAH",
				if 'Carrier_Id' in item:
					carrier_id = item['Carrier_Id'].lower()
				else:
					logger.error("Carrier ID missing from item!")
					logger.debug("%s", item)
					continue

				# TODO - Respect start and end time
				if carrier_id not in carriers:
					carriers[carrier_id] = {'products': [], 'available_states': dict(), 'available_insurance_types': [],
									        'available_products': [], 'additional_products': []}
				carrier = carriers[carrier_id]

				# "Carrier_Name": "Advantica",
				if 'Carrier_Name' in item and item['Carrier_Name'] != '':
					carrier_name = item['Carrier_Name']
					carrier['name'] = carrier_name
					carrier['slug'] = slugify(carrier_name + ' ' + carrier_id)
				# "CDM_Id": "a3Kg0000000KxoZEAS",
				if 'CDM_Id' in item and item['CDM_Id'] != '':
					carrier['cdm_id'] = item['CDM_Id']
				# "Website": "www.advanticabenefits.com",
				if 'Website' in item and item['Website'] != '':
					carrier['website_url'] = item['Website']
				# "Carrier_Description": ""
				if 'Carrier_Description' in item and item['Carrier_Description'] != '':
					carrier['description'] = item['Carrier_Description']
				# "Carrier_Logo_URL": "",
				if 'Carrier_Logo_URL' in item and item['Carrier_Logo_URL'] != '':
					carrier['logo_url'] = item['Carrier_Logo_URL']
				# "Carrier_Rating_Classification": "NR",
				if 'Carrier_Rating_Classification' in item and item['Carrier_Rating_Classification'] != '':
					carrier['rating_classification'] = item['Carrier_Rating_Classification']
				# "Carrier_Rating_Company_Name": "A. M. Best",
				if 'Carrier_Rating_Company_Name' in item and item['Carrier_Rating_Company_Name'] != '':
					carrier['rating_company_name'] = item['Carrier_Rating_Company_Name']
				# "Carrier_Rating_Description": "Not Rated",
				if 'Carrier_Rating_Description' in item and item['Carrier_Rating_Description'] != '':
					carrier['rating_description'] = item['Carrier_Rating_Description']
				# "Display_Start_Time": "2011-01-01T06:00:00.000Z",
				if 'Display_Start_Time' in item and item['Display_Start_Time'] != '':
					carrier['start_time'] = item['Display_Start_Time']
				# "Display_End_Time": "2020-03-24T17:00:00.000Z",
				if 'Display_End_Time' in item and item['Display_End_Time'] != '':
					carrier['end_time'] = item['Display_End_Time']

				# GATHER THESE AHEAD OF THE LOOP

				# "state": "Delaware",
				insurance_type = item['Insurance_Type']
				insurance_type_slug = slugify(insurance_type).replace('-', '_')
				state_name = item['state']
				quoting_available = item['Online_Quoting_Available']
				state = {'name': state_name}
				product_types = item['Product_Types'].split(';')
				if state_name not in carrier['available_states']:
					carrier['available_states'][state_name] = state
				else:
					state = carrier['available_states'][state_name]

				if insurance_type not in state:
					state[insurance_type] = {
						'quoting_available': quoting_available,
						'product_types': product_types,
					}

				# "Insurance_Type": "Small Group",
				for it in carrier['available_insurance_types']:
					if it['name'] == insurance_type:
						current_insurance_type = it
						break
				else:
					current_insurance_type = {'name': insurance_type, 'order': 6, 'quoting_available': quoting_available}
					if insurance_type in INSURANCE_TYPE_ORDER:
						current_insurance_type['order'] = INSURANCE_TYPE_ORDER[insurance_type]
					carrier['available_insurance_types'].append(current_insurance_type)
				if quoting_available:
					current_insurance_type['quoting_available'] = quoting_available
					carrier['show_quoting'] = 'True'

				# "Product_Types": "Dental;Vision",
				if insurance_type in INSURANCE_TYPE_ORDER:  # if it's one of the columns
					for product_type in product_types:
						for p in carrier['products']:
							if p['name'] == product_type:
								product = p
								break
						else:
							product = {'name': product_type, 'order': 6}
							if product_type in PRODUCT_ORDER:
								product['order'] = PRODUCT_ORDER[product_type]
							carrier['products'].append(product)
						if insurance_type_slug not in product:
							product[insurance_type_slug] = {'name': insurance_type, 'states': []}

						for s in product[insurance_type_slug]['states']:
							if s['name'] == state['name']:
								break
						else:
							product[insurance_type_slug]['states'].append(state)

				else:  # It's an additional product
					for product_type in product_types:
						if product_type not in carrier['additional_products']:
							carrier['additional_products'].append(product_type)

				for product_type in product_types:
					for ap in carrier['available_products']:
						if ap['name'] == product_type:
							product = ap
							break
					else:
						product = {'name': product_type, 'order': 6}
						if product_type in PRODUCT_ORDER:
							product['order'] = PRODUCT_ORDER[product_type]
						carrier['available_products'].append(product)

			cache.set(cachekey, carriers, None)
			logger.info('Successfully updated carrier cache')
		except Exception as ex:
			logger.error('Error updating carrier cache', ex)
