import json
import logging
from django.core.management.base import BaseCommand
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from api.models import Config


class Command(BaseCommand):

    help = 'Load config data into system'

    def handle(self, *args, **options):
        self.load_tasks()

    def __get_frequency_value(self, value):
        return int(value.split(' ')[0])

    def __get_frequency_unit(self, value):
        unit = value.split(' ')[1]
        if str.lower(unit) == 'seconds':
            return IntervalSchedule.SECONDS
        if str.lower(unit) == 'minutes':
            return IntervalSchedule.MINUTES
        if str.lower(unit) == 'hours':
            return IntervalSchedule.HOURS

    def load_tasks(self):
        with open('config.json', 'r') as f:
            try:
                json_data = json.load(f)
            except Exception as e:
                logging.critical("Unable to load config.json data")
                logging.critical(e)
        self.__create_monitors(json_data)
        self.__create_config(json_data)
        self.__create_task('_retention', 'tasks.celery.cleanup',  1, IntervalSchedule.HOURS, {})

    def __create_monitors(self, json_data):
        for k, v in json_data['monitor'].items():
            v['title'] = k
            self.__create_task(k, 'tasks.celery.rest', self.__get_frequency_value(v['frequency']), self.__get_frequency_unit(v['frequency']), v)

    def __create_config(self, json_data):
        for k, v in json_data['config'].items():
            try:
                config = Config.objects.get(key=k)
                config.value = v
                config.save()
            except Config.DoesNotExist:
                Config.objects.create(key=k, value=str(v))

    def __create_task(self, name, task, every, period, kwargs):
        schedule, created = IntervalSchedule.objects.get_or_create(every=every, period=period)
        try:
            PeriodicTask.objects.get(name=name)
            PeriodicTask.objects.filter(name=name).update(interval=schedule, task=task, enabled=True, kwargs=json.dumps(kwargs))
        except PeriodicTask.DoesNotExist:
            PeriodicTask.objects.create(interval=schedule, name=name, task=task, enabled=True, kwargs=json.dumps(kwargs))
