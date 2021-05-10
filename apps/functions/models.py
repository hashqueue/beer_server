from django.db import models

from project.models import Project
from utils.django_utils.base_model import BaseModel


# Create your models here.

class Function(BaseModel):
    function_name = models.CharField(max_length=150, verbose_name='全局函数名称', help_text='全局函数名称')
    function_desc = models.CharField(max_length=256, blank=True, default='', verbose_name='全局函数描述', help_text='全局函数描述')
    function_body = models.TextField(verbose_name='全局函数内容', help_text='全局函数内容')
    project = models.OneToOneField(to=Project, on_delete=models.CASCADE, verbose_name='所属项目', help_text='所属项目')

    class Meta:
        db_table = 'function_info'
        verbose_name = '全局函数'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.function_name
