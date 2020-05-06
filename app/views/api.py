from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponse, JsonResponse, Http404
import requests
import json
from django.core.cache import cache




PRODUCT_ORDER = {
    'Medical': 1,
    'Dental': 2,
    'Vision': 3,
    'Life': 4,
    'Disability': 5,
}
INSURANCE_TYPE_ORDER = {
    'Large Group': 1,
    'Small Group': 2,
    'Self-Funded': 3,
    'Individual': 4,
    'Senior': 5,
    'Additional': 6,
}

def carrier_json(request):
    cachekey = 'carriers'

    # # ret = cache.get(cachekey)
    # print(ret)
    # if not ret:
    #     print("cacheing")

    params = {
        'grant_type': 'password',
        'client_id': '3MVG9ahGHqp.k2_ysR5QacRbHlHN1WYdbcrNhiVY4aE48SzvpJWORIlSZnCR20LCgPE7BAIfPAZBt3sGyLPNP',
        'client_secret': 'DBCE6F4E5A79087E022DE97FE435DE8157D13FEC28AF66205A9A2611E24C9695',
        'username': 'insitein@benefitmall.com.devkasu',
        'password': 'Test@415sQk1D2vzH26ZwTBltnQxvnbD'
    }

    r = requests.post('https://test.salesforce.com/services/oauth2/token', params=params)
    access_token = r.json().get("access_token")
    instance_url = r.json().get("instance_url")

    headers = {
        'Content-type': 'application/json',
        'Accept-Encoding': 'gzip',
        'Authorization': 'Bearer %s' % access_token
    }

    r = requests.request('get',
                         instance_url + '/services/apexrest/CarrierAccounts/services/apexrest/CarrierAccounts/',
                         headers=headers,
                         params=params,
                         )
    ret = r.json()
    carriers = {}
    for item in ret:
        # "Carrier_Id": "001g000002ETUdlAAH",
        id = None
        if 'Carrier_Id' in item:
            id = item['Carrier_Id']

        # TODO - Respect start and end time
        if id not in carriers:
            carriers[id] = {'products': [], 'available_states': [], 'available_insurance_types': []}
        carrier = carriers[id]

        # "CDM_Id": "a3Kg0000000KxoZEAS",
        if 'CDM_Id' in item and item['CDM_Id'] != '':
            carrier['cdm_id'] = item['CDM_Id']
        # "Carrier_Name": "Advantica",
        if 'Carrier_Name' in item and item['Carrier_Name'] != '':
            carrier['name'] = item['Carrier_Name']
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


        # "Product_Types": "Dental;Vision",
        if 'Product_Types' in item:
            product_types = item['Product_Types'].split(';')

            # GATHER THESE AHEAD OF THE LOOP
            # "state": "Delaware",
            state_name = item['state']
            quoting_available = item['Online_Quoting_Available']
            state = {'name': state_name, 'quoting_available': quoting_available}
            if state_name not in carrier['available_states']:
                carrier['available_states'].append(state_name)

            # "Insurance_Type": "Small Group",
            insurance_type = item['Insurance_Type']
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

            for product_type in item['Product_Types'].split(';'):
                for p in carrier['products']:
                    if p['name'] == product_type:
                        product = p
                        break
                else:
                    product = {'name': product_type, 'order': 6}
                    if product_type in PRODUCT_ORDER:
                        product['order'] = PRODUCT_ORDER[product_type]
                    carrier['products'].append(product)
                if insurance_type not in product:
                    product[insurance_type] = {'name': insurance_type, 'states': []}
                product[insurance_type]['states'].append(state)


    # else:
    #     print("cached")

    return HttpResponse(json.dumps(carriers), content_type='text/json')
    # return HttpResponse(r.text, content_type='text/json')
    # return ret


