from django.db import models

# Create your models here.
class SomeModel(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    count = models.IntegerField(blank=True, default=10)
