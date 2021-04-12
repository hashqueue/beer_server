from rest_framework import permissions
from rest_framework.decorators import action

from utils.drf_utils.custom_json_response import JsonResponse
from .serializers import TestCaseSerializer, RunTestCaseSerializer
from .models import TestCase, TestStep
from utils.drf_utils.custom_model_view_set import CustomModelViewSet
from utils.http_utils.http_request import HttpSession


# Create your views here.

class TestCasesViewSet(CustomModelViewSet):
    queryset = TestCase.objects.filter(deleted=False).order_by('-id')
    serializer_class = TestCaseSerializer
    permission_classes = [permissions.IsAuthenticated]
    my_api_set_tags = ["用例管理"]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user.username, modifier=self.request.user.username)

    def perform_update(self, serializer):
        serializer.save(modifier=self.request.user.username)

    def perform_destroy(self, instance):
        instance.deleted = True
        instance.save()

    @action(methods=['post'], detail=True)
    def run(self, request, pk=None):
        teststep_objs = TestStep.objects.filter(testcase_id=pk)
        data = {}
        for teststep in teststep_objs:
            if '$' in teststep.url_path:
                # 设置了全局base_url
                pass
            else:
                resp = HttpSession.request(teststep.method, url=teststep.url_path)
                data.update(resp)
        return JsonResponse(data=data, code=20000, msg='运行成功')

    def get_serializer_class(self):
        return RunTestCaseSerializer if self.action == 'run' else TestCaseSerializer
