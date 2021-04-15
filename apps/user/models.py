from django.db import models
from django.contrib.auth.models import AbstractUser


def user_directory_path(instance, filename):
    """
    自定义用户头像保存路径为：static/media/images/user_<id>/<filename>
    """
    return f'{instance.user.id}/{filename}'


# Create your models here.
class User(AbstractUser):
    """
    用户表模型
    blank=True在字符串类型的字段上表现为空字符串，不是null
    """
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间', help_text='更新时间')
    avatar = models.ImageField(upload_to=user_directory_path, blank=True, default='/images/default/default.jpeg',
                               verbose_name='头像路径', help_text='头像路径')
    department = models.CharField(max_length=128, blank=True, default='', verbose_name='部门名称', help_text='部门名称')
    position = models.CharField(max_length=128, blank=True, default='', verbose_name='职位名称', help_text='职位名称')
    phone = models.CharField(max_length=11, blank=True, default='', verbose_name='手机号', help_text='手机号')

    class Meta:
        db_table = 'user_info'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
