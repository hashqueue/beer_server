from django.db import models

from project.models import Project
from utils.django_utils.base_model import BaseModel


# Create your models here.

class Config(BaseModel):
    config_name = models.CharField(max_length=150, verbose_name='配置名称', help_text='配置名称')
    config_desc = models.CharField(max_length=256, blank=True, verbose_name='配置描述', help_text='配置描述')
    project = models.ManyToManyField(to=Project, verbose_name='关联项目', help_text='关联项目')

    class Meta:
        db_table = 'config_info'
        verbose_name = '全局配置'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.config_name


class Variable(models.Model):
    var_key = models.CharField(max_length=128, blank=True, unique=True, verbose_name='全局变量的key', help_text='全局变量的key')
    var_value = models.TextField(blank=True, verbose_name='全局变量的value(全局变量值/jmespath表达式)',
                                 help_text='全局变量的value(全局变量值/jmespath表达式)')
    desc = models.CharField(max_length=512, blank=True, verbose_name='全局变量描述', help_text='全局变量描述')
    config = models.ForeignKey(to=Config, null=True, on_delete=models.SET_NULL, verbose_name='所属配置项',
                               related_name='config_variables',
                               help_text='所属配置项')

    class Meta:
        db_table = 'global_variable_info'
        verbose_name = '全局变量'
        verbose_name_plural = verbose_name
