from app.celery import app as tasks
from django.core.management import call_command


@tasks.task
def update_carrier_cache():
	call_command('update_carrier_data')