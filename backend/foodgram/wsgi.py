from django.core.wsgi import get_wsgi_application
# Сделал импорты поприятнее
import os



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'foodgram.settings')

application = get_wsgi_application()
