from django.contrib.auth.hashers import make_password
from django.db.models import Q
from rest_framework import serializers
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler

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
