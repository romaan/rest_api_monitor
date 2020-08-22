from django_celery_beat.models import PeriodicTask, IntervalSchedule
import json
import logging


def get_frequency_value(value):
    return int(value['frequencey'].split(' ')[0])


def get_frequency_unit(value):
    unit = value['frequency'].split(' ')[1]
    if str.lower(unit) == 'seconds':
        return IntervalSchedule.SECONDS
    if str.lower(unit) == 'minutes':
        return IntervalSchedule.MINUTES
    if str.lower(unit) == 'hours':
        return IntervalSchedule.HOURS


def load_tasks():
    with open('config.json', 'r') as f:
        data = f.readlines()
    try:
        jsonData = json.loads(data)
    except Exception as e:
        logging.critical("Unable to load config.json data")
        logging.critical(e)
    for k, v in jsonData:
        schedule, created = IntervalSchedule.objects.get_or_create(every=get_frequency_value(v), period=get_frequency_unit(v))
        try:
            PeriodicTask.objects.get(name=k)
            PeriodicTask.objects.filter(name=k).update(interval=schedule, task='tasks.rest')
        except PeriodicTask.DoesNotExist:
            PeriodicTask.objects.create(interval=schedule,  name=k, task='tasks.rest', args=json.dumps(['somevalue']))