from .base import *

DEBUG = env.bool('DJANGO_DEBUG', default=False)

# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Raises ImproperlyConfigured exception if DJANGO_SECRET_KEY not in os.environ
SECRET_KEY = env('DJANGO_SECRET_KEY')


# SITE CONFIGURATION
# ------------------------------------------------------------------------------
# Hosts/domain names that are valid for this site
# See https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=['stack-theme.herokuapp.com', ])
# END SITE CONFIGURATION

INSTALLED_APPS += ['gunicorn', ]

# Use Whitenoise to serve static files
# See: https://whitenoise.readthedocs.io/
WHITENOISE_MIDDLEWARE = ['whitenoise.middleware.WhiteNoiseMiddleware', ]
MIDDLEWARE = WHITENOISE_MIDDLEWARE + MIDDLEWARE


# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------

# Use the Heroku-style specification
# Raises ImproperlyConfigured exception if DATABASE_URL not in os.environ
DATABASES['default'] = env.db('DATABASE_URL')


# # ANYMAIL
# # ------------------------------------------------------------------------------
# # https://anymail.readthedocs.io/en/stable/installation/#installing-anymail
# INSTALLED_APPS += ['anymail']  # noqa F405
# EMAIL_BACKEND = 'anymail.backends.sendgrid.EmailBackend'
# # https://anymail.readthedocs.io/en/stable/installation/#anymail-settings-reference
# ANYMAIL = {
#     'SENDGRID_API_KEY': env('SENDGRID_API_KEY')
# }
DEFAULT_FROM_EMAIL = 'www_no-reply@benefitmall.com'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env.str('EMAIL_HOST', 'benefitmall-com.mail.protection.outlook.com')
EMAIL_PORT = env.str('EMAIL_PORT', '25')
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', True)
EMAIL_HOST_USER = env.str('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = env.str('EMAIL_HOST_PASSWORD', '')

# SECURITY SETTINGS - THESE SHOULD ALWAYS BE IN PRODUCTION
# ------------------------------------------------------------------------------
SECURE_HSTS_SECONDS = 31536000
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = 'DENY'
# DONT ENABLE THIS UNLESS YOU KNOW WHAT TO LOOK FOR
USE_CSP_HEADER = env.bool('USE_CSP_HEADER', default=False)
USE_CSP_EXCEPTIONS = env.list('USE_CSP_EXCEPTIONS', default=[])

# STORAGE CONFIGURATION
# ------------------------------------------------------------------------------
# Uploaded Media Files
# ------------------------
# See: http://django-storages.readthedocs.io/en/latest/index.html
INSTALLED_APPS += ['storages', ]

AWS_ACCESS_KEY_ID = env('BUCKETEER_AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('BUCKETEER_AWS_SECRET_ACCESS_KEY')          
AWS_STORAGE_BUCKET_NAME = env('BUCKETEER_BUCKET_NAME')
AWS_AUTO_CREATE_BUCKET = False
AWS_QUERYSTRING_AUTH = False

CHAT_BUTTON_ID = env('CHAT_BUTTON_ID')
CHAT_DEPLOYMENT_ID = env('CHAT_DEPLOYMENT_ID')
CHAT_ORG_ID = env('CHAT_ORG_ID')

# AWS cache settings, don't change unless you know what you're doing:
AWS_EXPIRY = 60 * 60 * 24 * 7

# TODO See: https://github.com/jschneier/django-storages/issues/47
# Revert the following and use str after the above-mentioned bug is fixed in
# either django-storage-redux or boto
control = 'max-age=%d, s-maxage=%d, must-revalidate' % (AWS_EXPIRY, AWS_EXPIRY)
AWS_HEADERS = {
    'Cache-Control': bytes(control, encoding='latin-1')
}

# URL that handles the media served from MEDIA_ROOT, used for managing
# stored files.
MEDIA_URL = 'https://%s.s3.amazonaws.com/public/' % AWS_STORAGE_BUCKET_NAME
AWS_LOCATION = 'public/'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'


# Static Assets
# ------------------------
LOCAL_STATIC = False
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

