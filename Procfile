web: newrelic-admin run-program gunicorn tlapp.wsgi --log-file -
worker: python manage.py worker
postprocesser: python manage.py postprocesser
release: python manage.py migrate