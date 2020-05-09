from django.contrib.auth import hashers
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager
from django.db import models

GENDER_MALE = 'M'
GENDER_FEMALE = 'F'
GENDER_CHOICE = (
    (GENDER_MALE, '男性'),
    (GENDER_FEMALE, '女性')
)

CHARACTER_CHOICE = (
    ('A', 'Admin'),
    ('U', 'User')
)


class UserModel(AbstractBaseUser):
    """ 用户表 """
    USERNAME_FIELD = 'id'

    name = models.CharField(max_length=255, help_text='名字')
    pinyin = models.CharField(max_length=255, help_text='名字拼音')
    password = models.CharField(max_length=255, help_text='密码')
    phone = models.BigIntegerField(unique=True, null=True, help_text='手机号')
    email = models.EmailField(unique=True, null=True, help_text='邮箱')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICE, default='M', help_text='性别')
    character = models.CharField(max_length=1, choices=CHARACTER_CHOICE, default='U', help_text='账号类型')
    objects = UserManager()

    class Meta:
        db_table = 'users'
        ordering = ['-id']

    def __str__(self):
        return '<UserModel {}>'.format(self.name)

    def check_password(self, raw_password):
        return hashers.check_password(raw_password, self.password)
