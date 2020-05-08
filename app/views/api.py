from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponse, JsonResponse, Http404
import requests
import json
from django.core.cache import cache
from django.utils.text import slugify
from django.conf import settings

############################## PROD SETTINGS ##############################
# CARRIER_API_URL = "https://benefitmall.my.salesforce.com"
# CARRIER_API_ENDPOINT = "/services/apexrest/CarrierAccounts/"
# CARRIER_API_AUTH_URL = "/services/oauth2/token"
# CARRIER_API_USER = "insitein@benefitmall.com"
# CARRIER_API_PASS = "Insite@430"
# CARRIER_API_TOKEN = "z4CxSuTWooLnmGgfLa7dZCEcI"
# CARRIER_API_CLIENT_ID = "3MVG98XJQQAccJQc67xDDomk9lYr3DW7CWigK8uC3PPFlbYgGOZpU1MLYfxqtP6JsNJNJMntokckbz99Daxg_"
# CARRIER_API_CLIENT_SECRET = "F6DA75835F1A15BD9C8884653294335041483166ED44DA0D934E6329E3F0B493"


############################## DEV SETTINGS ##############################
# CARRIER_API_URL = "https://benefitmall--DevKasu.cs17.my.salesforce.com"
# CARRIER_API_ENDPOINT = "/services/apexrest/CarrierAccounts/services/apexrest/CarrierAccounts/"
# CARRIER_API_AUTH_URL = "/services/oauth2/token"
# CARRIER_API_USER = "insitein@benefitmall.com.devkasu"
# CARRIER_API_PASS = "Test@415"
# CARRIER_API_TOKEN = "sQk1D2vzH26ZwTBltnQxvnbD"
# CARRIER_API_CLIENT_ID = "3MVG9ahGHqp.k2_ysR5QacRbHlHN1WYdbcrNhiVY4aE48SzvpJWORIlSZnCR20LCgPE7BAIfPAZBt3sGyLPNP"
# CARRIER_API_CLIENT_SECRET = "DBCE6F4E5A79087E022DE97FE435DE8157D13FEC28AF66205A9A2611E24C9695"

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

def carrier_json(request):
    cachekey = 'carriers'

    cache.clear()
    ret = cache.get(cachekey)
    if not ret:

        params = {
            'grant_type': 'password',
            'client_id': settings.CARRIER_API_CLIENT_ID,
            'client_secret': settings.CARRIER_API_CLIENT_SECRET,
            'username': settings.CARRIER_API_USER,
            'password': settings.CARRIER_API_PASS+settings.CARRIER_API_TOKEN,
        }

        r = requests.post(settings.CARRIER_API_URL+settings.CARRIER_API_AUTH_URL, params=params)
        access_token = r.json().get("access_token")
        instance_url = r.json().get("instance_url")

        headers = {
            'Content-type': 'application/json',
            'Accept-Encoding': 'gzip',
            'Authorization': 'Bearer %s' % access_token
        }

        r = requests.request('get',
                             instance_url + settings.CARRIER_API_ENDPOINT,
                             headers=headers,
                             params=params,
                             )
        ret = r.json()
        carriers = {}
        for item in ret:
            # "Carrier_Id": "001g000002ETUdlAAH",
            id = None
            if 'Carrier_Id' in item:
                id = item['Carrier_Id'].lower()

            # TODO - Respect start and end time
            if id not in carriers:
                carriers[id] = {'products': [], 'available_states': [], 'available_insurance_types': [], 'available_products': [], 'additional_products': []}
            carrier = carriers[id]

            # "Carrier_Name": "Advantica",
            if 'Carrier_Name' in item and item['Carrier_Name'] != '':
                carrier_name = item['Carrier_Name']
                carrier['name'] = carrier_name
                carrier['slug'] = slugify(carrier_name + ' ' + id)

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
            state_name = item['state']
            quoting_available = item['Online_Quoting_Available']
            state = {'name': state_name, 'quoting_available': quoting_available}
            if state_name not in carrier['available_states']:
                carrier['available_states'].append(state_name)

            # "Insurance_Type": "Small Group",
            insurance_type = item['Insurance_Type']
            insurance_type_slug = slugify(insurance_type).replace('-','_')
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
            product_types = item['Product_Types'].split(';')
            if insurance_type in INSURANCE_TYPE_ORDER: #  if it's one of the columns
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

            else: # It's an additional product
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
        ret = carriers
        cache.set(cachekey, carriers, None)

    else:
        tmp = 'already cached'
        new_tmp = tmp


    return HttpResponse(json.dumps(ret), content_type='text/json')
    # return HttpResponse(r.text, content_type='text/json')
    # return ret


