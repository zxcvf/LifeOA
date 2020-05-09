"""自定义管理命令"""
from django.core.management.base import BaseCommand
from django.contrib.auth import hashers

from users.models import UserModel, GENDER_MALE


class Command(BaseCommand):
    """自定义管理命令，创建初始Admin帐号"""

    def handle(self, *args, **options):
        admin = UserModel(
            name='admin',
            pinyin='admin',
            phone='15116381393',
            email='673554003@qq.com',
            gender=GENDER_MALE,
            password=hashers.make_password('123456'),
        )
        admin.save()
        self.stdout.write(self.style.SUCCESS('添加Admin帐号成功'))
