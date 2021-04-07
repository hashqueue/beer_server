from django.db import models
from utils.django_utils.base_model import BaseModel


# Create your models here.

class Project(BaseModel):
    project_name = models.CharField(max_length=150, verbose_name='项目名称', help_text='项目名称')
    project_desc = models.CharField(max_length=256, blank=True, verbose_name='项目描述', help_text='项目描述')

    class Meta:
        db_table = 'project_info'
        verbose_name = '项目'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.project_name
