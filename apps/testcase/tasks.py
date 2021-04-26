# -*- coding: utf-8 -*-
# @Time    : 2021/4/26 下午9:02
# @Author  : anonymous
# @File    : tasks.py
# @Software: PyCharm
# @Description:

from celery import shared_task
from testcase.models import TestCase


@shared_task
def add(x, y):
    return x + y


@shared_task
def count_testcases():
    return TestCase.objects.count()
