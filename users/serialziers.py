from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.core.cache import cache
from rest_framework import serializers
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler
from utils import tasks
from utils.func_utils import get_random_string
from LifeOA.exceptions import CustomAPIException
from users.models import UserModel
from utils.serializers import DataSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        exclude = ('password',)


class LoginSerializer(DataSerializer):
    account = serializers.CharField(max_length=255, required=True, help_text='手机或邮箱')
    password = serializers.CharField(max_length=255, required=True, help_text='密码')

    def login(self):
        user = UserModel.objects.filter(Q(phone=self.validated_data['account']) |
                                        Q(email=self.validated_data['account'])).first()

        if user and user.check_password(self.validated_data['password']):
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)

            info_serializer = self.context.get('info_serializer')(instance=user)
            return {
                'token': token,
                **info_serializer.data
            }
        raise CustomAPIException(400, '密码错误')


class UpdatePwdSerializer(serializers.ModelSerializer):
    """ 验证码修改密码 """

    code = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = UserModel
        fields = ('password', 'code', 'email')

    def validate(self, attrs):
        if UserModel.objects.filter(email=attrs['email']).exists() \
                and cache.get(attrs['email']):
            return attrs
        raise CustomAPIException(400, '该用户不存在或激活码已过期')

    def reset(self):
        user = UserModel.objects.get(email=self.validated_data['email'])
        user.password = make_password(self.validated_data['password'])
        user.save(update_fields=['password'])


class ResetSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(required=True, help_text='新密码')

    class Meta:
        model = UserModel
        fields = ('password', 'new_password')

    def validate(self, attrs):
        if self.instance.check_password(attrs['password']):
            return {'password': make_password(attrs['new_password'])}
        raise CustomAPIException(400, '密码错误')

    def reset(self):
        self.update(
            self.instance,
            self.validated_data
        )


class ForgotSerializer(DataSerializer):
    """ 忘记密码 发送邮件 """
    email = serializers.EmailField(required=True)

    def send_email(self):
        code = get_random_string(6)
        print(code)
        msg = """
            你好, 你的验证码为{}。
            过期时间为60秒，请及时使用
        """.format(code)
        tasks.send_email.delay(msg, self.validated_data['email'], '忘记密码')
        cache.set(key=self.validated_data['email'],
                  value=code,
                  timeout=60)  # token延时
