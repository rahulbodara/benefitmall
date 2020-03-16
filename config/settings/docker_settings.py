from .dev import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'app_db',
        'USER': 'app_user',
        'PASSWORD': 'changeme',
        'HOST': 'db',
        'PORT': '5432'
    }
}