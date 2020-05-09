from django.shortcuts import render

# Create your views here.
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from LifeOA.permissions import perm_login
from users.models import UserModel
from users.serialziers import LoginSerializer, UserSerializer, ResetSerializer, ForgotSerializer, UpdatePwdSerializer


class AuthViewSet(GenericViewSet, ):
    """登陆认证接口"""

    class _Permission(BasePermission):
        def has_permission(self, request, view):
            if view.action in ['reset']:
                return perm_login(request)
            return True

    serializer_class = UserSerializer
    permission_classes = (_Permission,)
    queryset = UserModel.objects.all()

    @swagger_auto_schema(tags=['Auth'], operation_summary='手机号/邮箱登录',
                         request_body=LoginSerializer,
                         responses=None)
    @action(methods=['POST'], detail=False)
    def login(self, request, *args, **kwargs):
        """登录"""
        serializer = LoginSerializer(data=request.data,
                                     context={'info_serializer': self.get_serializer_class()})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.login())

    @swagger_auto_schema(tags=['Auth'], operation_summary='修改密码',
                         request_body=ResetSerializer,
                         responses=None)
    @action(methods=['POST'], detail=False)
    def reset(self, request, *args, **kwargs):
        """修改密码"""
        serializer = ResetSerializer(
            self.request.user,
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.reset()
        return Response('success')

    @swagger_auto_schema(tags=['Auth'], operation_summary='发送忘记密码邮件',
                         request_body=ForgotSerializer,
                         responses=None)
    @action(methods=['POST'], detail=False)
    def send_forgot(self, request, *args, **kwargs):
        """ 发送重置密码邮件 """
        serializer = ForgotSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.send_email()
        return Response('success')

    @swagger_auto_schema(tags=['Auth'], operation_summary='忘记密码',
                         request_body=UpdatePwdSerializer,
                         responses=None)
    @action(methods=['POST'], detail=False)
    def forgot(self, request, *args, **kwargs):
        """ 根据邮件验证码重置密码 """
        serializer = UpdatePwdSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.reset()
        return Response('success')
