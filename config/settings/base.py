# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import environ
env = environ.Env()
from django.utils.translation import gettext_lazy as _

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PROJECT_NAME = os.path.basename(BASE_DIR)

# Application definition

INSTALLED_APPS = [
    # 'wagtail_modeltranslation',
    # 'wagtail_modeltranslation.makemigrations',
    # 'wagtail_modeltranslation.migrate',

    'app',

    'wagtail.contrib.forms',
    'wagtail.contrib.modeladmin',
    'wagtail.contrib.redirects',
    'wagtail.contrib.settings',
    'wagtail.contrib.postgres_search',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail.core',

    'modelcluster',
    'honeypot',
    'wagtailfontawesome',
    'taggit',
    'site_settings',
    'widget_tweaks',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',


]


MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',

    'site_settings.middleware.SecurityMiddleware',
    'site_settings.middleware.CaseInsensitiveURLMiddleware',
    'site_settings.middleware.SiteSettingsMiddleware',
    'wagtail.core.middleware.SiteMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',

    'app.middleware.NavigationItemRedirectMiddleware',

    'honeypot.middleware.HoneypotMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'app/templates'),
            os.path.join(BASE_DIR, 'site_settings/templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'wagtail.contrib.settings.context_processors.settings',
                'site_settings.context_processors.get_site_meta_data',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'carrier_data',
    }
}

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': PROJECT_NAME,
    },
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]



# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'app/locale'),
)

LANGUAGE_CODE = 'en'

LANGUAGES = (
    ('en', _('English')),
)

TIME_ZONE = 'America/Chicago'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATICFILES_FINDERS = [
    # 'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'app/static'),
]

LOCAL_STATIC = True

STATIC_ROOT = os.path.join(BASE_DIR, 'assets')
STATIC_URL = '/assets/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


# Wagtail settings

WAGTAIL_SITE_NAME = PROJECT_NAME

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
BASE_URL = 'http://www.benefitmall.com'

# django-honeypot - provides utilities for preventing automated form spam.
HONEYPOT_FIELD_NAME = 'official_title'

WAGTAIL_ENABLE_UPDATE_CHECK = False

# Disable this to avoid loading over http
WAGTAIL_GRAVATAR_PROVIDER_URL = None

WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtail.contrib.postgres_search.backend',
        'INDEX': 'wagtail',
        'TIMEOUT': 5,
        'OPTIONS': {},
        'INDEX_SETTINGS': {},
        'ATOMIC_REBUILD': True,
    }
}

############################## PROD SETTINGS ##############################
# CARRIER_API_URL = "https://benefitmall.my.salesforce.com"
# CARRIER_API_ENDPOINT = "/services/apexrest/CarrierAccounts/"
# CARRIER_API_AUTH_URL = "/services/oauth2/token"
# CARRIER_API_USER = "insitein@benefitmall.com"
# CARRIER_API_PASS = "Insite@630"
# CARRIER_API_TOKEN = "scjeY3VNzHvxhNrVz1T4Kvpz"
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

SHOW_CARRIER_API_DATA = env.bool('SHOW_CARRIER_API_DATA', False)

CARRIER_API_URL = env.str('CARRIER_API_URL', 'https://benefitmall.my.salesforce.com')
CARRIER_API_ENDPOINT = env.str('CARRIER_API_ENDPOINT', '/services/apexrest/CarrierAccounts/')
CARRIER_API_AUTH_URL = env.str('CARRIER_API_AUTH_URL', '/services/oauth2/token')
CARRIER_API_USER = env.str('CARRIER_API_USER', 'insitein@benefitmall.com')
CARRIER_API_PASS = env.str('CARRIER_API_PASS', 'InsiteReset@630')
CARRIER_API_TOKEN = env.str('CARRIER_API_TOKEN', 'scjeY3VNzHvxhNrVz1T4Kvpz')
CARRIER_API_CLIENT_ID = env.str('CARRIER_API_CLIENT_ID', '3MVG98XJQQAccJQc67xDDomk9lYr3DW7CWigK8uC3PPFlbYgGOZpU1MLYfxqtP6JsNJNJMntokckbz99Daxg_')
CARRIER_API_CLIENT_SECRET = env.str('CARRIER_API_CLIENT_SECRET', 'F6DA75835F1A15BD9C8884653294335041483166ED44DA0D934E6329E3F0B493')


# Updated credentials
# Password: InsiteReset@630
# Security token: scjeY3VNzHvxhNrVz1T4Kvpz

# CHAT PROD
# Chat Button ID: 5731L000000M5rP
# Chat Deployment: 5721L000000M4Hq
# Chat Org Identifier: 00DG0000000gEcp
# CHAT DEV
# Chat Button ID: 573c0000000CbCw
# Chat Deployment: 572c0000000Casl
# Chat Org Identifier: 00Dc0000003wW7y

CHAT_BUTTON_ID = '5731L000000M5rP'
CHAT_DEPLOYMENT_ID = '5721L000000M4Hq'
CHAT_ORG_ID = '00DG0000000gEcp'


#LEAD GEN FORM
LEAD_GEN_FORM_URL = env.str('LEAD_GEN_FORM_URL', 'https://test.salesforce.com/servlet/servlet.WebToLead?encoding=UTF-8')
LEAD_GEN_FORM_OID = env.str('LEAD_GEN_FORM_OID', '00Dc0000003wW7y')


CELERY_BROKER_URL = env('REDIS_URL', default='redis://localhost:6379')
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
TRIGGERS_ON = env('TRIGGERS_ON', default=True)

AWS_ACCESS_KEY_ID = 'AKIAVVKH7VVUFNCC7QG4'
AWS_REGION = 'us-east-1'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'bucketeer-ea354d00-8d1c-4da1-ac86-0d2f739b43e6'
DATA_UPLOAD_MAX_NUMBER_FIELDS = None
