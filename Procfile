release: python manage.py migrate --noinput
sudo daphne --ws-protocol src.asgi:application --port 80 --bind 0.0.0.0 -v2
sudo python manage.py runworker -v2