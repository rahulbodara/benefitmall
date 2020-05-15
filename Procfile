release: yes "yes" | python manage.py migrate && python manage.py update_index
web: gunicorn config.wsgi_heroku --log-file -
worker: celery worker --beat --app=app --loglevel=info -Ofair
