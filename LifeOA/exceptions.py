"""自定义视图与接口相关辅助类"""
import traceback

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import Http404, JsonResponse
from rest_framework import exceptions, status
from rest_framework.views import set_rollback


class CustomAPIException(Exception):
    """业务异常类"""

    code = status.HTTP_500_INTERNAL_SERVER_ERROR
    message = ''

    def __init__(self, code=None, message=None):
        super().__init__()
        if code is not None:
            self.code = code
        if message is not None:
            self.message = message


def error_response(code=0, message='', data=None):
    """错误数据返回"""
    wrapped_data = {
        'status': 'error',
        'code': code,
        'data': data,
        'message': message,
        'meta': settings.META_MSG
    }
    return JsonResponse(wrapped_data)


def exception_handler(exc, context):
    """异常处理"""
    print('error')
    traceback.print_exc()
    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    if isinstance(exc, exceptions.NotAuthenticated):
        set_rollback()
        return error_response(status.HTTP_401_UNAUTHORIZED, exc.__class__.__name__)

    if isinstance(exc, CustomAPIException):
        set_rollback()
        return error_response(exc.code, exc.message)

    if isinstance(exc, exceptions.ValidationError):
        set_rollback()
        return error_response(exc.status_code, next(iter(next(iter(exc.detail.values())))))

    if isinstance(exc, exceptions.APIException):
        set_rollback()
        return error_response(exc.status_code, exc.__class__.__name__)

    return None
