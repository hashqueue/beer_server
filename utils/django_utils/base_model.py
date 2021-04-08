# -*- coding: utf-8 -*-
# @Time    : 2021/3/14 下午5:35
# @Author  : anonymous
# @File    : base_model.py
# @Software: PyCharm
# @Description:
from django.db import models


class BaseModel(models.Model):
    '''
    数据库表公共字段
    '''
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', help_text='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间', help_text='更新时间')
    deleted = models.BooleanField(default=False, verbose_name='逻辑删除(值为true表示已删除,为false表示未被删除)',
                                  help_text='逻辑删除(值为true表示已删除,为false表示未被删除)')
    creator = models.CharField(max_length=150, verbose_name='创建人', help_text='创建人')
    modifier = models.CharField(max_length=150, verbose_name='最后修改人', help_text='最后修改人')

    class Meta:
        # 设置当前模型类为抽象类，用于其他模型类来继承，数据库迁移时不会创建当前模型类的表
        abstract = True
        verbose_name = '公共字段表'
