from .base import *

DEBUG = True
SHOW_CARRIER_API_DATA = True
# USE_CSP_HEADER = True
# USE_CSP_EXCEPTIONS = 'jquery,typekit,googlefonts,googlemaps,youtube,gtm,gtm_preview,gtm_custom_vars,salesforce,vidyard'


#SECRET_KEY = '8*p^q5c)7^&6wi62p^n$a#t+9et(##28k$&m^jrinf!wqmq)%2'
from dotenv import load_dotenv
load_dotenv()
env = os.getenv

DJANGO_SECRET_KEY = env('DJANGO_SECRET_KEY')

SECRET_KEY = DJANGO_SECRET_KEY

ALLOWED_HOSTS = ['*']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

INSTALLED_APPS += [
    'wagtail.contrib.styleguide',
    #'faker',
    #'django_nose',
    #'model_mommy',
]

try:
    from .local import *
except ImportError:
    pass
