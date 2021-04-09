# -*- coding: utf-8 -*-
# @Time    : 2021/4/7 下午11:01
# @Author  : anonymous
# @File    : signals.py
# @Software: PyCharm
# @Description:
from django.dispatch import Signal, receiver

# 自定义信号
update_testcase_to_deleted_signal = Signal(providing_args=['testsuite_instance'])


@receiver(update_testcase_to_deleted_signal)
def update_testcase_to_deleted_signal_callback(sender, **kwargs):
    """
    删除套件后，通过信号机制设置该套件下关联的数据的状态为已删除：deleted=True
    """
    testcase_objs = kwargs['testsuite_instance'].testcase_set.all()
    if len(testcase_objs) > 0:
        for testcase in testcase_objs:
            testcase.deleted = True
            testcase.save()
