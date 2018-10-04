# -*- coding:utf-8 -*-

from __future__ import absolute_import
from celery.schedules import crontab

CELERY_RESULT_BACKEND = 'redis://192.168.43.218:6379/0'
BROKER_URL = 'redis://192.168.43.218:6379/0'

CELERY_TIMEZONE = 'Asia/Shanghai'

from datetime import timedelta
'''
CELERYBEAT_SCHEDULE = { 'add-every-10-seconds': {
                            'task': 'cele.tasks.add',
                            'schedule': timedelta(seconds=10),
                            'args': (16, 16) },
                        }
'''
CELERYBEAT_SCHEDULE = { 'add-every-60-seconds': {
                            'task': 'cele.tasks.add',
                            'schedule': crontab(),#以整数分钟开始计时，如果不是整数，立马执行一次，至整数分钟时再执行一次，后面都是整数分钟了
                            'args': (16, 16) },
                        }
'''
from celery.schedules import crontab

# 每分钟执行一次
c1 = crontab()

# 每天凌晨十二点执行
c2 = crontab(minute=0, hour=0)

# 每十五分钟执行一次
crontab(minute='*/15')

# 每周日的每一分钟执行一次
crontab(minute='*',hour='*', day_of_week='sun')

# 每周三，五的三点，七点和二十二点没十分钟执行一次
crontab(minute='*/10',hour='3,17,22', day_of_week='thu,fri')


'''