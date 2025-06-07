from django.apps import AppConfig
# PEP8


class ShortenerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shortener'
    verbose_name = 'Сопоставленные ссылки'
