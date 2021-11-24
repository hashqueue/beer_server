from django.db.models import Q
from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework import status

from .serializers import ProjectSerializer, RunProjectSerializer
from .models import Project
from config.models import Config
from .tasks import run_project
from utils.drf_utils.custom_permissions import IsObjectCreatorOrModifierInRequestUserGroups
from utils.drf_utils.custom_json_response import enveloper, JsonResponse


# Create your views here.
@extend_schema(tags=['项目管理'])
class ProjectsViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsObjectCreatorOrModifierInRequestUserGroups]
    filterset_fields = ['project_name', 'project_desc', 'creator', 'modifier']

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user.username, modifier=self.request.user.username)

    def perform_update(self, serializer):
        serializer.save(modifier=self.request.user.username)

    def get_queryset(self):
        if self.request.user.is_superuser is True:
            return Project.objects.all().order_by('-id')
        else:
            users_list = []
            for group_obj in self.request.user.groups.all():
                for user_obj in group_obj.user_set.all():
                    users_list.append(user_obj.username)
            # 当前登录用户所在的所有的用户组中所关联的所有用户集合(去重处理)
            users_set = list(set(users_list))
            queryset = Project.objects.filter(Q(creator__in=users_set) & Q(modifier__in=users_set)).distinct().order_by(
                '-id')
            return queryset

    @extend_schema(responses=enveloper(RunProjectSerializer, False))
    @action(methods=['post'], detail=True, serializer_class=RunProjectSerializer)
    def run(self, request, pk=None):
        """
        运行项目
        @todo 权限管理依赖于action为list的数据集进行控制,如果通过接口运行不在此数据集中的项目也是可以运行的
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if request.data.get('config_id', False):
            # 选择某个项目来运行项目
            async_result = run_project.delay(project_id=get_object_or_404(Project, pk=pk).id,
                                             config_id=get_object_or_404(Config, pk=request.data.get('config_id')).id,
                                             creator=request.user.username,
                                             creator_email=request.user.email)
            return JsonResponse(data={"task_id": async_result.task_id}, code=20000,
                                msg=f'启动运行项目任务成功,任务id为{async_result.task_id},请稍后查看任务运行结果',
                                status=status.HTTP_202_ACCEPTED)
        else:
            # 不选择项目直接执行项目
            async_result = run_project.delay(project_id=get_object_or_404(Project, pk=pk).id,
                                             creator=request.user.username,
                                             creator_email=request.user.email)
            return JsonResponse(data={"task_id": async_result.task_id}, code=20000,
                                msg=f'启动运行项目任务成功,任务id为{async_result.task_id},请稍后查看任务运行结果',
                                status=status.HTTP_202_ACCEPTED)

    @extend_schema(responses=enveloper(ProjectSerializer, False))
    def create(self, request, *args, **kwargs):
        """
        新增项目
        """
        res = super().create(request, *args, **kwargs)
        return JsonResponse(data=res.data, msg='success', code=20000, status=status.HTTP_201_CREATED,
                            headers=res.headers)

    @extend_schema(responses=enveloper(ProjectSerializer, True))
    def list(self, request, *args, **kwargs):
        """
        获取项目列表

        `响应体数据格式以下方示例为准`
        ```json
        # 当响应状态码为200时(response_code = 200)
        {
          "code": 20000,
          "message": "success",
          "data": {
            "count": 16,
            "next": "http://127.0.0.1:8000/api/projects/?page=2&size=1",
            "previous": null,
            "results": [
              {
                "id": 0,
                "create_time": "2019-08-24T14:15:22Z",
                "update_time": "2019-08-24T14:15:22Z",
                "creator": "string",
                "modifier": "string",
                "project_name": "string",
                "project_desc": "string"
              },
              {
                "id": 0,
                "create_time": "2019-08-24T14:15:22Z",
                "update_time": "2019-08-24T14:15:22Z",
                "creator": "string",
                "modifier": "string",
                "project_name": "string",
                "project_desc": "string"
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

    @extend_schema(responses=enveloper(ProjectSerializer, False))
    def retrieve(self, request, *args, **kwargs):
        """
        查看项目详情
        """
        res = super().retrieve(request, *args, **kwargs)
        return JsonResponse(data=res.data, msg='success', code=20000, status=status.HTTP_200_OK)

    @extend_schema(responses=enveloper(ProjectSerializer, False))
    def update(self, request, *args, **kwargs):
        """
        更新项目
        """
        res = super().update(request, *args, **kwargs)
        return JsonResponse(data=res.data, msg='success', code=20000)

    @extend_schema(responses=enveloper(ProjectSerializer, False))
    def partial_update(self, request, *args, **kwargs):
        """
        更新项目
        """
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        删除项目
        """
        return super().destroy(request, *args, **kwargs)

    