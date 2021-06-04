from django.db import models

from project.models import Project
from utils.django_utils.base_model import BaseModel


# Create your models here.

class Config(BaseModel):
    config_name = models.CharField(max_length=150, verbose_name='配置名称', help_text='配置名称')
    config_desc = models.CharField(max_length=256, blank=True, default='', verbose_name='配置描述', help_text='配置描述')
    global_variable = models.JSONField(verbose_name='全局变量', help_text='全局变量')
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE, verbose_name='所属项目ID', help_text='所属项目ID')

    class Meta:
        db_table = 'config_info'
        verbose_name = '全局配置'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.config_name
