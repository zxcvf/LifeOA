from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
from datetime import timedelta

from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LifeOA.settings')
app = Celery('LifeOA')


# app.config_from_object('django.conf:settings', namespace='CELERY')

class Config:
    broker_url = settings.REDIS
    # todo 暂时不使用
    result_backend = settings.REDIS
    accept_content = ['application/json']
    task_serializer = 'json'
    result_serializer = 'json'
    timezone = 'Asia/Shanghai'
    tasks_per_child = 100


# 可能是因为path 为orange/backend的问题无法读取django.conf:settings
# app.config_from_object('django.conf:settings', namespace='CELERY')
app.config_from_object(Config)

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# 添加crontab 任务
app.conf.update(
    CELERYBEAT_SCHEDULE={
    },
)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
