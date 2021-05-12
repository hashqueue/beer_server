from drf_spectacular.utils import extend_schema
from rest_framework import permissions
from django.contrib.auth.models import Group

from .serializers import GroupSerializer
from utils.drf_utils.custom_model_view_set import MyListRetrieveModelViewSet


# Create your views here.
@extend_schema(tags=['用户组管理'])
class GroupsViewSet(MyListRetrieveModelViewSet):
    queryset = Group.objects.all().order_by('-id')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
