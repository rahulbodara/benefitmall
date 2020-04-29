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
    ret = r.json()
    out = []
    carriers = {}
    insurance_types = []
    product_types = []
    carrier_names = []
    for item in ret:
        carrier = {}

        # "Website": "www.advanticabenefits.com",
        # "state": "Delaware",
        # "Product_Types": "Dental;Vision",
        # "Online_Quoting_Available": false,
        # "Insurance_Type": "Large Group",
        # TODO - Respect start and end time
        # "Display_Start_Time": "2011-01-01T06:00:00.000Z",
        # "Display_End_Time": "2020-03-24T17:00:00.000Z",
        # "Carrier_Rating_Description": "Not Rated",
        # "Carrier_Rating_Company_Name": "A. M. Best",
        # "Carrier_Rating_Classification": "NR",
        # "Carrier_Name": "Advantica",
        # "Carrier_Logo_URL": "https://benefitmall--c.na76.content.force.com/sfc/dist/version/renditionDownload?rendition=ORIGINAL_JPG&versionId=0681L000007pZ9JQAU&operationContext=DELIVERY&contentId=null&page=0&d=/a/1L0000001Asq/J5zWUtAsIERyq6m5HPOPmZGhInfQH1MIl4wLptZ0qdE&oid=00DG0000000gEcpMAE",
        # "Carrier_Description": "<p>Custom Description for Advantica Delaware</p>"

        if 'state' in item:
            carrier['state'] = item['state']
        if 'Website' in item:
            carrier['website_url'] = item['Website']
        if 'Insurance_Type' in item:
            carrier['insurance_type'] = item['Insurance_Type']
        if 'Product_Types' in item:
            carrier['product_types'] = item['Product_Types']
        if 'Online_Quoting_Available' in item:
            carrier['quoting_available'] = item['Online_Quoting_Available']
        if 'Carrier_Name' in item:
            carrier['name'] = item['Carrier_Name']
        if 'Carrier_Description' in item:
            carrier['description'] = item['Carrier_Description']
        if 'Carrier_Logo_URL' in item:
            carrier['logo_url'] = item['Carrier_Logo_URL']
        if 'Carrier_Rating_Classification' in item:
            carrier['rating_classification'] = item['Carrier_Rating_Classification']
        if 'Carrier_Rating_Company_Name' in item:
            carrier['rating_company_name'] = item['Carrier_Rating_Company_Name']
        if 'Carrier_Rating_Description' in item:
            carrier['rating_description'] = item['Carrier_Rating_Description']
        out.append(carrier)
        if 'insurance_type' in carrier:
            insurance_types.append(carrier['insurance_type'])
        if 'product_types' in carrier:
            product_types.extend(carrier['product_types'].split(';'))
        if 'name' in carrier:
            carrier_names.append(carrier['name'])
    # carriers[carrier['carrier_id']] = carrier
    insurance_types = list(set(insurance_types))
    product_types = list(set(product_types))
    carrier_names = list(set(carrier_names))

    # else:
    #     print("cached")

    return HttpResponse(json.dumps(out), content_type='text/json')
    # return HttpResponse(r.text, content_type='text/json')
    # return ret


