# backend/apps.py

from django.apps import AppConfig

class BackendConfig(AppConfig):
    name = 'backend'

    def ready(self):
        # We will initialize the scheduler separately
        pass
