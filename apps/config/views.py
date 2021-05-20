from django.db.models import Q
from drf_spectacular.utils import extend_schema
from rest_framework import permissions

from .serializers import ConfigSerializer
from .models import Config
from utils.drf_utils.custom_model_view_set import CustomModelViewSet
from utils.drf_utils.custom_permissions import IsObjectCreatorOrModifierInRequestUserGroups


# Create your views here.
@extend_schema(tags=['配置管理'])
class ConfigsViewSet(CustomModelViewSet):
    serializer_class = ConfigSerializer
    permission_classes = [permissions.IsAuthenticated, IsObjectCreatorOrModifierInRequestUserGroups]
    filterset_fields = ['config_name', 'config_desc', 'creator', 'modifier', 'project']

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user.username, modifier=self.request.user.username)

    def perform_update(self, serializer):
        serializer.save(modifier=self.request.user.username)

    def get_queryset(self):
        if self.request.user.is_superuser is True:
            return Config.objects.all().order_by('-id')
        else:
            users_list = []
            for group_obj in self.request.user.groups.all():
                for user_obj in group_obj.user_set.all():
                    users_list.append(user_obj.username)
            # 当前登录用户所在的所有的用户组中所关联的所有用户集合(去重处理)
            users_set = list(set(users_list))
            queryset = Config.objects.filter(Q(creator__in=users_set) & Q(modifier__in=users_set)).distinct().order_by(
                '-id')
            return queryset
