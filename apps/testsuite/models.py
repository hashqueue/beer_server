from django.db import models
from utils.django_utils.base_model import BaseModel
from project.models import Project


# Create your models here.

class TestSuite(BaseModel):
    testsuite_name = models.CharField(max_length=150, verbose_name='套件名称', help_text='套件名称')
    testsuite_desc = models.CharField(max_length=256, blank=True, default='', verbose_name='套件描述', help_text='套件描述')
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE, verbose_name='所属项目ID', help_text='所属项目ID')

    class Meta:
        db_table = 'testsuite_info'
        verbose_name = '测试套件'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.testsuite_name
