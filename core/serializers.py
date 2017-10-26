# coding: utf-8
from rest_framework import serializers
from . import models


class Generate(serializers.Serializer):
    VOICE_CHOICES = (
        ('anna', 'Anna'),
        ('elena', 'Elena'),
        ('irina', 'Irina'),
    )

    voice = serializers.ChoiceField(choices=VOICE_CHOICES)
    text = serializers.CharField()


class Voice(serializers.Serializer):
    uuid = serializers.UUIDField()

    def validate_uuid(self, value):
        if not models.Voice.objects.filter(uuid=value).exists():
            raise serializers.ValidationError('File with id {} not found.'.format(value))
        return value
