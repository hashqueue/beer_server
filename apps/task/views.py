from django.db.models import Q
from drf_spectacular.utils import extend_schema
from rest_framework import permissions
from django_celery_results.models import TaskResult

from .serializers import TaskSerializer
from utils.drf_utils.custom_model_view_set import MyListRetrieveDestroyModelViewSet


# Create your views here.
@extend_schema(tags=['测试任务管理'])
class TasksViewSet(MyListRetrieveDestroyModelViewSet):
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
            # 当前登录用户所在的所有的用户组中所关联的所有用户集合
            users_set = list(set(users_list))
            queryset_list = []
            for user in users_set:
                queryset = TaskResult.objects.filter(task_kwargs__contains=user).order_by('-id')
                queryset_list.extend(queryset)
            return list(set(queryset_list))
