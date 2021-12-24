from django.apps import AppConfig


class EegtestConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'eegtest'

    def ready(self):
        import eegtest.signals
