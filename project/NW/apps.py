from django.apps import AppConfig


class NwConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'NW'

    def ready(self):
        from . import signals  # выполнение модуля -> регистрация сигналов