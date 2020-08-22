from django.apps import AppConfig
import json
import logging
import os

class ApiConfig(AppConfig):
    name = 'api'

    def ready(self):
        self.load_tasks()

    def get_frequency_value(self, value):
        return int(value['frequency'].split(' ')[0])

    def get_frequency_unit(self, value):
        from django_celery_beat.models import IntervalSchedule
        unit = value['frequency'].split(' ')[1]
        if str.lower(unit) == 'seconds':
            return IntervalSchedule.SECONDS
        if str.lower(unit) == 'minutes':
            return IntervalSchedule.MINUTES
        if str.lower(unit) == 'hours':
            return IntervalSchedule.HOURS

    def load_tasks(self):
        from django_celery_beat.models import PeriodicTask, IntervalSchedule
        with open('config.json', 'r') as f:
            try:
                jsonData = json.load(f)
            except Exception as e:
                logging.critical("Unable to load config.json data")
                logging.critical(e)
        for k, v in jsonData.items():
            schedule, created = IntervalSchedule.objects.get_or_create(every=self.get_frequency_value(v),
                                                                       period=self.get_frequency_unit(v))
            try:
                PeriodicTask.objects.get(name=k)
                PeriodicTask.objects.filter(name=k).update(interval=schedule, task='tasks.rest')
            except PeriodicTask.DoesNotExist:
                PeriodicTask.objects.create(interval=schedule, name=k, task='tasks.rest',
                                            args=json.dumps(['somevalue']))
