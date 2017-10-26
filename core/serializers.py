import subprocess

from rest_framework import serializers
from django.core.files.uploadedfile import TemporaryUploadedFile

from core.datatools import string
from core import consts
from core import models


class Generate(serializers.ModelSerializer):
    voice = serializers.ChoiceField(choices=consts.VOICE_CHOICES, default='anna')

    class Meta:
        model = models.Voice
        fields = ('text', 'voice')

    def create(self, validated_data):
        text = validated_data['text']
        voice = validated_data['voice']
        filename = '{}.wav'.format(string.random_string(10))

        with TemporaryUploadedFile(filename, None, None, None) as temp:
            echo = subprocess.Popen(['echo', text], stdout=subprocess.PIPE)
            rhvoice = subprocess.Popen(['RHVoice-test',
                                        '-p', voice,
                                        '-o', temp.temporary_file_path()],
                                       stdin=echo.stdout, stdout=subprocess.PIPE)

            instance = None
            if echo.wait() == 0 and rhvoice.wait() == 0:
                instance = models.Voice.objects.create(text=text, file=temp)

        return rhvoice.returncode, instance


class Voice(serializers.ModelSerializer):
    class Meta:
        model = models.Voice
        fields = ('uuid', 'file')
