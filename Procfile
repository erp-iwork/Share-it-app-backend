release: python manage.py migrate --noinput
web: daphne src.asgi:application --port 8000 --bind 0.0.0.0  -v2
worker: python manage.py runworker -v2