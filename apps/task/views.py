from drf_spectacular.utils import extend_schema
from rest_framework import permissions
from django_celery_results.models import TaskResult
from rest_framework import status

from .serializers import TaskSerializer
from utils.drf_utils.custom_model_view_set import MyListRetrieveDestroyModelViewSet
from utils.drf_utils.custom_json_response import enveloper, JsonResponse


# Create your views here.
@extend_schema(tags=['测试任务管理'])
class TasksViewSet(MyListRetrieveDestroyModelViewSet):
    queryset = TaskResult.objects.none()  # 无效变量，纯粹是为了接口文档不报错
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    # 默认pk为id字段，通过lookup_field替换id字段为task_id
    lookup_field = 'task_id'

    def get_queryset(self):
        if self.request.user.is_superuser is True:
            return TaskResult.objects.all().order_by('-id')
        else:
            users_list = []
            for group_obj in self.request.user.groups.all():
                for user_obj in group_obj.user_set.all():
                    users_list.append(user_obj.username)
            # 当前登录用户 所在的所有的用户组中 所关联的所有用户 的集合
            # 默认展示当前用户 所在用户组内 所有组员的数据
            users_set = list(set(users_list))
            queryset = TaskResult.objects.filter(task_kwargs__contains=users_set[0]).order_by('-id')
            for user in users_set[1:]:
                queryset = queryset | TaskResult.objects.filter(task_kwargs__contains=user).order_by('-id')
            # print(queryset)
            return queryset

    @extend_schema(responses=enveloper(TaskSerializer, True))
    def list(self, request, *args, **kwargs):
        """
        获取测试任务列表

        `响应体数据格式以下方示例为准`
        ```json
        # 当响应状态码为200时(response_code = 200)
        {
          "code": 20000,
          "message": "success",
          "data": {
            "count": 16,
            "next": "http://127.0.0.1:8000/api/tasks/?page=2&size=1",
            "previous": null,
            "results": [
              {
                "id": 0,
                "date_created": "2019-08-24T14:15:22Z",
                "date_done": "2019-08-24T14:15:22Z",
                "task_id": "string",
                "task_name": "string",
                "task_args": "string",
                "task_kwargs": "string",
                "status": "FAILURE",
                "worker": "string",
                "content_type": "string",
                "content_encoding": "string",
                "result": "string",
                "traceback": "string",
                "meta": "string"
              },
              {
                "id": 0,
                "date_created": "2019-08-24T14:15:22Z",
                "date_done": "2019-08-24T14:15:22Z",
                "task_id": "string",
                "task_name": "string",
                "task_args": "string",
                "task_kwargs": "string",
                "status": "FAILURE",
                "worker": "string",
                "content_type": "string",
                "content_encoding": "string",
                "result": "string",
                "traceback": "string",
                "meta": "string"
              },
            ],
            "total_pages": 16,
            "current_page": 1
          }
        }
        ```
        """
        res = super().list(request, *args, **kwargs)
        return JsonResponse(data=res.data, msg='success', code=20000)

    @extend_schema(responses=enveloper(TaskSerializer, False))
    def retrieve(self, request, *args, **kwargs):
        """
        查看测试任务详情
        """
        res = super().retrieve(request, *args, **kwargs)
        return JsonResponse(data=res.data, msg='success', code=20000, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """
        删除测试任务
        """
        return super().destroy(request, *args, **kwargs)

