from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponse, JsonResponse, Http404
import requests
import json
from django.core.cache import cache



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
    ret = json.loads(r.json())
    out = []
    carriers = {}
    insurance_types = []
    product_types = []
    carrier_names = []
    for item in ret:
        carrier = {}

        if 'State__c' in item:
            carrier['state'] = item['State__c']
        if 'Id' in item:
            carrier['carrier_id'] = item['Id']
        if 'Insurance_Type__c' in item:
            carrier['insurance_type'] = item['Insurance_Type__c']
        if 'Product_Types__c' in item:
            carrier['product_types'] = item['Product_Types__c']
        if 'Online_Quoting_Available__c' in item:
            carrier['quoting_available'] = item['Online_Quoting_Available__c']
        if 'Carrier_Acct__r' in item:
            if 'Name' in item['Carrier_Acct__r']:
                carrier['name'] = item['Carrier_Acct__r']['Name']
            if 'Carrier_Description__c' in item['Carrier_Acct__r']:
                carrier['description'] = item['Carrier_Acct__r']['Carrier_Description__c']
            if 'Carrier_Logo_URL__c' in item['Carrier_Acct__r']:
                carrier['logo_url'] = item['Carrier_Acct__r']['Carrier_Logo_URL__c']
            if 'Carrier_Rating_Classification__c' in item['Carrier_Acct__r']:
                carrier['rating_classification'] = item['Carrier_Acct__r']['Carrier_Rating_Classification__c']
            if 'Carrier_Rating_Company_Name__c' in item['Carrier_Acct__r']:
                carrier['rating_company_name'] = item['Carrier_Acct__r']['Carrier_Rating_Company_Name__c']
            if 'Carrier_Rating_Description__c' in item['Carrier_Acct__r']:
                carrier['rating_description'] = item['Carrier_Acct__r']['Carrier_Rating_Description__c']
        out.append(carrier)
        if carrier['insurance_type']:
            insurance_types.append(carrier['insurance_type'])
        if carrier['product_types']:
            product_types.extend(carrier['product_types'].split(';'))
        if carrier['name']:
            carrier_names.append(carrier['name'])
    # carriers[carrier['carrier_id']] = carrier
    insurance_types = list(set(insurance_types))
    product_types = list(set(product_types))
    carrier_names = list(set(carrier_names))

    # else:
    #     print("cached")

    return HttpResponse(json.dumps(out), content_type='text/json')
    # return ret


