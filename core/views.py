# Create your views here.
import subprocess
import os
import uuid

from django.http import Http404, JsonResponse
from django.http import HttpResponse
from django.conf import settings
from django.core.files import File

from rest_framework.response import Response
from rest_framework.decorators import api_view

from core.models import Wav


@api_view(['post'])
def generate_speech(request):
    """Создание wav файла с переданным текстом
    ---
    parameters:
    - name: text
      description: Текст который преобразовать в wav
      required: true
      type: text
      paramType: form
    """
    text = request.POST.get('text')
    if not text:
        return JsonResponse({'status': 'error', 'output': u'No text parameter'})

    if Wav.objects.filter(text=text).exists():
        wav = Wav.objects.filter(text=text).first()
        return JsonResponse({'output': 'Already generated', 'uuid': wav.uuid})

    wav = Wav(text=text)
    file_out = '%s/%s.wav' % (settings.WAV_TMP_DIR, wav.uuid)
    command = 'echo %s | RHVoice-test -p elena -o %s' % (text, file_out)
    wav.command = command
    status, output = subprocess.getstatusoutput(command)
    path_to_generated_file = os.path.join(settings.BASE_DIR, file_out)
    f = open(path_to_generated_file, "rb")
    wav.file = File(f)
    wav.save()
    status, output = subprocess.getstatusoutput('rm %s' % path_to_generated_file)

    return JsonResponse({'status': status, 'output': output, 'uuid': wav.uuid})


@api_view()
def play_speech(request):
    """Получение wav файла по uuid
    ---
    parameters:
    - name: uuid
      description: uuid4
      required: true
      type: text
      paramType: query
    """

    uuid_text = request.GET.get('uuid')

    try:
        uuid_ = uuid.UUID(uuid_text)
    except ValueError:
        return Response({'status': 'error', 'message': '%s - Not correct uuid4 format' % uuid_text})

    try:
        wavs = Wav.objects.get(uuid=uuid_)

        f = wavs.file

        response = HttpResponse()
        response.write(f.file.read())

        response['Content-Type'] = 'audio/vnd.wave'
        response['Content-Length'] = f.size
        response['Content-Disposition'] = 'attachment; filename=%s' % f.name.split('/')[-1]

        return response
    except Wav.DoesNotExist:
        raise Http404
