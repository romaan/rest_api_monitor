from __future__ import absolute_import, unicode_literals
from celery import Celery
import os
# replace app.settings with your django settings.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webapp.settings')
app = Celery('schedule-tasks', broker='redis://localhost:6379/0',
include=['tasks.tasks'])
if __name__ == '__main__':
        app.start()