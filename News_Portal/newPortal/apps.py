from django.apps import AppConfig


class NewportalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'newPortal'

    def ready(self):
        from . import signals  # выполнение модуля -> регистрация сигналов