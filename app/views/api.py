from django.shortcuts import render
from django.core import serializers
from app.models.salesforce import Account


def carrier_data(request):

    data = serializers.serialize("python", Account.objects.filter(type='Carrier'))
    context = {
        'carriers': data
    }

    return render(request, 'carrier_data.html', context)