import os
import channels

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings")
application = channels.asgi.get_channel_layer()
