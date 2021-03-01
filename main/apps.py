from django.apps import AppConfig


class MainConfig(AppConfig):
    name = 'main'

    # Registering a signal
    def ready(self):
    	from . import signals
