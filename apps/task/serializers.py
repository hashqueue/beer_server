# -*- coding: utf-8 -*-
# @Time    : 2021/4/7 下午5:23
# @Author  : anonymous
# @File    : serializers.py
# @Software: PyCharm
# @Description:
from django_celery_results.models import TaskResult
from rest_framework import serializers


class TaskSerializer(serializers.ModelSerializer):
    date_created = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True, help_text='创建时间')
    date_done = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True, help_text='完成时间')

    class Meta:
        model = TaskResult
        fields = '__all__'
        read_only_fields = ('id', 'task_name', 'task_args', 'task_kwargs', 'status', 'worker', 'content_type',
                            'content_encoding', 'result', 'traceback', 'meta')
