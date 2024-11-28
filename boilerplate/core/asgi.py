import os
from pathlib import Path

from blacknoise import BlackNoise
from django.conf import settings
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

BASE_DIR = Path(__file__).parent

application = BlackNoise(get_asgi_application())
application.add(settings.STATIC_ROOT, settings.STATIC_URL)
