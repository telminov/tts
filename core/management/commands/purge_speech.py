import time

from django.core.management.base import BaseCommand
from django.utils.timezone import now
from django.conf import settings

from core import models


class Command(BaseCommand):
    help = 'Purge expired speech.'

    def add_arguments(self, parser):
        parser.add_argument('-i', '--infinitely', dest='infinitely', action='store_true')

    def handle(self, *args, **options):
        infinitely = options.get('infinitely')

        while True:
            dead_line = now() - settings.SPEECH_TTL
            models.Speech.objects.filter(dc__lte=dead_line).delete()

            if infinitely:
                time.sleep(60*10)   # every 10 minutes
            else:
                return
