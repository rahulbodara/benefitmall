release: yes "yes" | python manage.py migrate
web: gunicorn config.wsgi_heroku --log-file -
