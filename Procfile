release: python manage.py migrate --noinput
daphne  src.asgi:application --port 80 --bind 0.0.0.0 -v2
