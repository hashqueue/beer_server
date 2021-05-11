from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404

from .serializers import ProjectSerializer, RunProjectSerializer
from .models import Project
from config.models import Config
from utils.drf_utils.custom_model_view_set import CustomModelViewSet
from utils.drf_utils.custom_json_response import JsonResponse
from .tasks import run_project


# Create your views here.
@extend_schema(tags=['项目管理'])
class ProjectsViewSet(CustomModelViewSet):
    queryset = Project.objects.all().order_by('-id')
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user.username, modifier=self.request.user.username)

    def perform_update(self, serializer):
        serializer.save(modifier=self.request.user.username)

    @action(methods=['post'], detail=True, serializer_class=RunProjectSerializer)
    def run(self, request, pk=None):
        """
        启动运行项目任务
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if request.data.get('config_id', False):
            # 选择某个配置来运行项目
            async_result = run_project.delay(project_id=get_object_or_404(Project, pk=pk).id,
                                             config_id=get_object_or_404(Config, pk=request.data.get('config_id')).id,
                                             creator=request.user.username)
            return JsonResponse(data={"task_id": async_result.task_id}, code=20000,
                                msg=f'启动运行项目任务成功,任务id为{async_result.task_id},请稍后查看任务运行结果',
                                status=status.HTTP_200_OK)
        else:
            # 不选择配置直接执行项目
            async_result = run_project.delay(project_id=get_object_or_404(Project, pk=pk).id,
                                             creator=request.user.username)
            return JsonResponse(data={"task_id": async_result.task_id}, code=20000,
                                msg=f'启动运行项目任务成功,任务id为{async_result.task_id},请稍后查看任务运行结果',
                                status=status.HTTP_200_OK)
