from rest_framework import permissions
from django_celery_results.models import TaskResult

from .serializers import TaskSerializer
from utils.drf_utils.custom_model_view_set import MyListRetrieveDestroyModelViewSet


# Create your views here.

class TasksViewSet(MyListRetrieveDestroyModelViewSet):
    queryset = TaskResult.objects.all().order_by('-id')
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    my_api_set_tags = ["测试任务管理"]
