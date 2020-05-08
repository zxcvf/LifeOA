from django.conf import settings
from rest_framework.renderers import JSONRenderer


class CustomJSONRenderer(JSONRenderer):
    """自定义JSON返回数据"""

    def render(self, data, accepted_media_type=None, renderer_context=None):
        wrapped_data = {
            'status': 'success',
            'code': 2000,
            'data': data,
            'message': '',
            'meta': settings.META_MSG
        }
        return super().render(wrapped_data, accepted_media_type, renderer_context)


