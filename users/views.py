from django.shortcuts import render

# Create your views here.
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from users.serialziers import LoginSerializer, UserSerializer


class AuthViewSet(GenericViewSet):
    """登陆认证接口"""

    serializer_class = UserSerializer
    permission_classes = ()

    @swagger_auto_schema(tags=['登录'], operation_summary='手机号/邮箱登录',
                         request_body=LoginSerializer,
                         responses=None)
    @action(methods=['POST'], detail=False)
    def login(self, request, *args, **kwargs):
        """登录"""
        serializer = LoginSerializer(data=request.data, context={'info_serializer': self.get_serializer_class()})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.login())
