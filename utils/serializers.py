from rest_framework import serializers


class DataSerializer(serializers.Serializer):
    """只用户请求数据序列化"""

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class EmptySerializer(DataSerializer):
    """ 无字段 """

