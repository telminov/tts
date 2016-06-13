# -*- encoding: utf-8
import uuid

from django.db import models
from django.conf import settings


class SomeModel(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    count = models.IntegerField(blank=True, default=10)


class Wav(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255, blank=True)
    file = models.FileField(verbose_name=u'Файл', upload_to=settings.WAV_STORAGE_DIR)
    text = models.TextField(verbose_name=u'Фраза', blank=False)
    config = models.CharField(max_length=255, blank=True)
    command = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return '%s' % self.uuid

    class Meta:
        verbose_name = u'Созданный wav'
        verbose_name_plural = u'Созданные wav'
