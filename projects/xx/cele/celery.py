# -*- coding:utf-8 -*-

from __future__ import absolute_import
from celery import Celery

app = Celery('cele', include=['cele.tasks'])

app.config_from_object('cele.config')

if __name__ == '__main__':
    app.start()


