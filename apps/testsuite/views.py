from django.db.models import Q
from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework import status

from config.models import Config
from .serializers import TestSuiteSerializer, RunTestSuiteSerializer
from .models import TestSuite
from .tasks import run_testsuite
from utils.drf_utils.custom_permissions import IsObjectCreatorOrModifierInRequestUserGroups
from utils.drf_utils.custom_json_response import enveloper, JsonResponse


# Create your views here.
@extend_schema(tags=['套件管理'])
class TestSuitesViewSet(ModelViewSet):
    serializer_class = TestSuiteSerializer
    permission_classes = [permissions.IsAuthenticated, IsObjectCreatorOrModifierInRequestUserGroups]
    filterset_fields = ['testsuite_name', 'testsuite_desc', 'creator', 'modifier', 'project']

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user.username, modifier=self.request.user.username)

    def perform_update(self, serializer):
        serializer.save(modifier=self.request.user.username)

    def get_queryset(self):
        if self.request.user.is_superuser is True:
            return TestSuite.objects.all().order_by('-id')
        else:
            users_list = []
            for group_obj in self.request.user.groups.all():
                for user_obj in group_obj.user_set.all():
                    users_list.append(user_obj.username)
            # 当前登录用户所在的所有的用户组中所关联的所有用户集合(去重处理)
            users_set = list(set(users_list))
            queryset = TestSuite.objects.filter(
                Q(creator__in=users_set) & Q(modifier__in=users_set)).distinct().order_by(
                '-id')
            return queryset

    @extend_schema(responses=enveloper(RunTestSuiteSerializer, False))
    @action(methods=['post'], detail=True, serializer_class=RunTestSuiteSerializer)
    def run(self, request, pk=None):
        """
        启动运行测试套件任务
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if request.data.get('config_id', False):
            # 选择某个配置来运行测试套件
            async_result = run_testsuite.delay(testsuite_id=get_object_or_404(TestSuite, pk=pk).id,
                                               config_id=get_object_or_404(Config, pk=request.data.get('config_id')).id,
                                               creator=request.user.username,
                                               creator_email=request.user.email)
            return JsonResponse(data={"task_id": async_result.task_id}, code=20000,
                                msg=f'启动运行测试套件任务成功,任务id为{async_result.task_id},请稍后查看任务运行结果',
                                status=status.HTTP_202_ACCEPTED)
        else:
            # 不选择配置直接执行测试套件
            async_result = run_testsuite.delay(testsuite_id=get_object_or_404(TestSuite, pk=pk).id,
                                               creator=request.user.username,
                                               creator_email=request.user.email)
            return JsonResponse(data={"task_id": async_result.task_id}, code=20000,
                                msg=f'启动运行测试套件任务成功,任务id为{async_result.task_id},请稍后查看任务运行结果',
                                status=status.HTTP_202_ACCEPTED)

    @extend_schema(responses=enveloper(TestSuiteSerializer, False))
    def create(self, request, *args, **kwargs):
        """
        新增套件
        """
        res = super().create(request, *args, **kwargs)
        return JsonResponse(data=res.data, msg='success', code=20000, status=status.HTTP_201_CREATED,
                            headers=res.headers)

    @extend_schema(responses=enveloper(TestSuiteSerializer, True))
    def list(self, request, *args, **kwargs):
        """
        获取套件列表

        `响应体数据格式以下方示例为准`
        ```json
        # 当响应状态码为200时(response_code = 200)
        {
          "code": 20000,
          "message": "success",
          "data": {
            "count": 16,
            "next": "http://127.0.0.1:8000/api/groups/?page=2&size=1",
            "previous": null,
            "results": [
              {
                "id": 0,
                "create_time": "2019-08-24T14:15:22Z",
                "update_time": "2019-08-24T14:15:22Z",
                "project_name": "string",
                "creator": "string",
                "modifier": "string",
                "testsuite_name": "string",
                "testsuite_desc": "string",
                "project": 0
              },
              {
                "id": 0,
                "create_time": "2019-08-24T14:15:22Z",
                "update_time": "2019-08-24T14:15:22Z",
                "project_name": "string",
                "creator": "string",
                "modifier": "string",
                "testsuite_name": "string",
                "testsuite_desc": "string",
                "project": 0
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

    @extend_schema(responses=enveloper(TestSuiteSerializer, False))
    def retrieve(self, request, *args, **kwargs):
        """
        查看套件详情
        """
        res = super().retrieve(request, *args, **kwargs)
        return JsonResponse(data=res.data, msg='success', code=20000, status=status.HTTP_200_OK)

    @extend_schema(responses=enveloper(TestSuiteSerializer, False))
    def update(self, request, *args, **kwargs):
        """
        更新套件
        """
        res = super().update(request, *args, **kwargs)
        return JsonResponse(data=res.data, msg='success', code=20000)

    @extend_schema(responses=enveloper(TestSuiteSerializer, False))
    def partial_update(self, request, *args, **kwargs):
        """
        更新套件
        """
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        删除套件
        """
        return super().destroy(request, *args, **kwargs)

    