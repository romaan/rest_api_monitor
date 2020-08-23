from django.apps import AppConfig
import json
import logging
import os

class ApiConfig(AppConfig):
    name = 'api'

    def ready(self):
        # self.load_tasks()
        pass

