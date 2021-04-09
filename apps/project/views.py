from rest_framework import permissions

from .serializers import ProjectSerializer
from .models import Project
from .signals import update_testsuite_to_deleted_signal
from utils.drf_utils.custom_model_view_set import CustomModelViewSet


# Create your views here.

class ProjectsViewSet(CustomModelViewSet):
    queryset = Project.objects.filter(deleted=False).order_by('-id')
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]
    my_api_set_tags = ["项目管理"]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user.username, modifier=self.request.user.username)

    def perform_update(self, serializer):
        serializer.save(modifier=self.request.user.username)

    def perform_destroy(self, instance):
        instance.deleted = True
        instance.save()
        # 删除项目后，通过信号机制设置该项目下关联的数据的状态为已删除：deleted=True
        update_testsuite_to_deleted_signal.send(sender=Project, project_instance=instance)
