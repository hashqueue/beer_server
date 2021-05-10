from drf_spectacular.utils import extend_schema
from rest_framework import permissions
from django_celery_results.models import TaskResult

from .serializers import TaskSerializer
from utils.drf_utils.custom_model_view_set import MyListRetrieveDestroyModelViewSet


# Create your views here.
@extend_schema(tags=['测试任务管理'])
class TasksViewSet(MyListRetrieveDestroyModelViewSet):
    queryset = TaskResult.objects.all().order_by('-id')
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
