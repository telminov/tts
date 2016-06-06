from rest_framework import serializers
from core.models import SomeModel

class SomeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SomeModel
        fields = ('id', 'name', 'description', 'count')


    # def update(self, instance, validated_data):
    #     raise ValueError(u'IN UPDATE!!!')
    #     # instance.email = validated_data.get('email', instance.email)
    #     # instance.content = validated_data.get('content', instance.content)
    #     # instance.created = validated_data.get('created', instance.created)
    #     return instance