from django.http import HttpResponse
from simple_salesforce import Salesforce

def get_sf_data(request):
    sf = Salesforce(instance_url='https://benefitmall--DevKasu.cs17.my.salesforce.com/services/apexrest/CarrierAccounts/services/apexrest/CarrierAccounts/', session_id='00Dg0000006VWv4!AQcAQB81YAS6M5189zngbPEWkVmzZO1ph_VL.3sHe7Ex60BmQMPjzN.U13Z8_m1tSggXDCn9vmNeYQFZfPC9aOrzn2eRKltv')
    desc = sf.describe()
    field_names = [field['name'] for field in desc['fields']]
    soql = "SELECT {} FROM Account".format(','.join(field_names))
    results = sf.query_all(soql)
