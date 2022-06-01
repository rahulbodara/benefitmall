from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from app.management.commands.update_carrier_data import Command as carrier_update_command

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')

app = Celery('app')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(['app',])

if settings.TRIGGERS_ON:
    if settings.DEBUG:
        # For debug
        app.conf.beat_schedule = {
            'daily-every-5minutes': {
                'task': 'app.tasks.update_carrier_cache',
                'schedule': 300.0,
            },
        }
        pass
    else:
        # For production
        app.conf.beat_schedule = {
            'daily-every-5minutes': {
                'task': 'app.tasks.update_carrier_cache',
                'schedule': 300.0,
            },
        }
