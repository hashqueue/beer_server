from drf_spectacular.utils import extend_schema
from rest_framework import permissions
from django_celery_results.models import TaskResult

from .serializers import TaskSerializer
from utils.drf_utils.custom_model_view_set import MyListRetrieveDestroyModelViewSet


# Create your views here.
@extend_schema(tags=['测试任务管理'])
class TasksViewSet(MyListRetrieveDestroyModelViewSet):
    queryset = TaskResult.objects.none()  # 无效变量，纯粹是为了接口文档不报错
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

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
