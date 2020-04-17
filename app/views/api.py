import requests
import json
from django.core.cache import cache


def carrier_json():
    cachekey = 'carriers'

    ret = cache.get(cachekey)
    print(ret)
    if not ret:
        print("cacheing")
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
    else:
        print("cached")

    return ret


