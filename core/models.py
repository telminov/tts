# -*- encoding: utf-8
import uuid

from django.db import models
from django.conf import settings


class Voice(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    file = models.FileField(upload_to=settings.OUTPUT_DIR)
    text = models.TextField()

    dc = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}...'.format(self.text.capitalize()[:20])
