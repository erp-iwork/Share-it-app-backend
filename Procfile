release: python manage.py migrate --noinput
web: gunicorn src.wsgi
web2: daphne src.asgi:channel_layer --port 8000 --bind 0.0.0.0