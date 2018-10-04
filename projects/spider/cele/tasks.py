# -*- coding:utf-8 -*-

from __future__ import absolute_import
from cele.celery import app
import time
from taobao_test import main


@app.task
def add(x, y):
    t = main()
    return t