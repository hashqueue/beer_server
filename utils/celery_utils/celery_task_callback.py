# @ProjectName: beer_server
# @FileName: celery_task_callback.py
# @Author: www
# @Time: 2021/11/24 下午6:54
from django.core.mail import send_mail
from celery import Task as CTask
from beer_server.settings import config as config_file


class MyCeleryTask(CTask):

    def on_success(self, retval, task_id, args, kwargs):
        html_text = f"""<!DOCTYPE html>
        <html lang="zh">
        <head>
          <meta charset="UTF-8">
          <title>Title</title>
        </head>
        <body>
        <p>Hi，您启动的接口测试任务已运行完成，请点击
          <a href="{config_file.get_string_value('email', 'FE_TASK_DETAIL_BASEURL')}{task_id}"
             style="color: red; text-decoration: none;" target="_blank">测试报告详情</a>进行查看。
        </p>
        </body>
        </html>
        """
        creator_email = kwargs.get('creator_email')
        # 发送测试报告链接到当前任务创建者的邮箱里
        send_mail('接口测试报告', '接口测试报告', None, [creator_email], html_message=html_text)
        
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        # print(exc)
        # print(einfo)
        html_text = f"""<!DOCTYPE html>
        <html lang="zh">
        <head>
          <meta charset="UTF-8">
          <title>Title</title>
        </head>
        <body>
        <p>Hi，您启动的接口测试任务运行失败：{exc}. 错误详情如下：</p>
        <hr/>
        <p>{einfo}</p>
        </body>
        </html>
        """
        creator_email = kwargs.get('creator_email')
        # 发送测试报告链接到当前任务创建者的邮箱里
        send_mail('接口测试报告', '接口测试报告', None, [creator_email], html_message=html_text)
