import os

from blacknoise import BlackNoise
from django.conf import settings
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = BlackNoise(get_asgi_application())
application.add(settings.STATIC_ROOT, '/static/')
