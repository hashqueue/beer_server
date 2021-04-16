from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework.decorators import action

from config.models import Config
from utils.drf_utils.custom_json_response import JsonResponse
from .serializers import TestCaseSerializer, RunTestCaseSerializer
from .models import TestCase
from utils.drf_utils.custom_model_view_set import CustomModelViewSet
from utils.http_utils.request import run_testcase


# Create your views here.

class TestCasesViewSet(CustomModelViewSet):
    queryset = TestCase.objects.all().order_by('-id')
    serializer_class = TestCaseSerializer
    permission_classes = [permissions.IsAuthenticated]
    my_api_set_tags = ["用例管理"]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user.username, modifier=self.request.user.username)

    def perform_update(self, serializer):
        serializer.save(modifier=self.request.user.username)

    @action(methods=['post'], detail=True, serializer_class=RunTestCaseSerializer)
    def run(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if request.data.get('config_id', False):
            # 选择某个配置来执行用例
            run_testcase(testcase=get_object_or_404(TestCase, pk=pk),
                         config=get_object_or_404(Config, pk=request.data.get('config_id')))
        else:
            # 不选择配置直接执行用例
            run_testcase(testcase=get_object_or_404(TestCase, pk=pk))
        data = {"msg": "success"}
        return JsonResponse(data=data, code=20000, msg='运行成功')
