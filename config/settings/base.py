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
    'site_settings.middleware.SiteSettingsMiddleware',
    'site_settings.middleware.CaseInsensitiveURLMiddleware',
    'wagtail.core.middleware.SiteMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
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
                'site_settings.context_processors.site_settings',
                'site_settings.context_processors.meta_data',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': PROJECT_NAME,
    }
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

TIME_ZONE = 'UTC'

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
BASE_URL = 'http://localhost:8000'

# django-honeypot - provides utilities for preventing automated form spam.
HONEYPOT_FIELD_NAME = 'official_title'

WAGTAIL_ENABLE_UPDATE_CHECK = False

# Disable this to avoid loading over http
# WAGTAIL_GRAVATAR_PROVIDER_URL = None
