# -*- coding: utf-8 -*-
# @Time    : 2021/4/7 下午11:01
# @Author  : anonymous
# @File    : signals.py
# @Software: PyCharm
# @Description:
from django.dispatch import Signal, receiver

# 自定义信号
update_testsuite_to_deleted_signal = Signal(providing_args=['project_instance'])


@receiver(update_testsuite_to_deleted_signal)
def update_testsuite_to_deleted_signal_callback(sender, **kwargs):
    """
    删除项目后，通过信号机制设置该项目下关联的数据的状态为已删除：deleted=True
    """
    testsuite_objs = kwargs['project_instance'].testsuite_set.all()
    if len(testsuite_objs) > 0:
        for testsuite in testsuite_objs:
            testsuite.deleted = True
            testsuite.save()
            for testcase in testsuite.testcase_set.all():
                testcase.deleted = True
                testcase.save()
