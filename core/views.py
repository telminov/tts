# Create your views here.
import subprocess
import os
import uuid

from django.http import Http404, JsonResponse
from django.http import HttpResponse
from django.conf import settings
from django.core.files import File

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework import status

from core.models import SomeModel, Wav
from core.serializers import SomeModelSerializer


class SomeModelList(APIView):
    """Список объектов SomeModel.
        This text is the description for this API
        param1 -- A first parameter
        param2 -- A second parameter
    """
    def get(self, request, format=None):
        some_models = SomeModel.objects.all()
        serializer = SomeModelSerializer(some_models, many=True)
        return Response(serializer.data)


    def post(self, request, format=None):
        """Создает объектов SomeModel"""
        serializer = SomeModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SomeModelDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return SomeModel.objects.get(pk=pk)
        except SomeModel.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        some_model = self.get_object(pk)
        serializer = SomeModelSerializer(some_model)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SomeModelSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class SomeModelViewSet(viewsets.ModelViewSet):
    """Вью СЕТ!

    """
    serializer_class = SomeModelSerializer
    queryset = SomeModel.objects.all()

@api_view(['post'])
def generate_speach(request):
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
        return Response({'status': 'error','output': u'No text parameter'})

    if Wav.objects.filter(text=text):
        wav = Wav.objects.filter(text=text).first()
        return Response({'output': 'Already generated', 'uuid': wav.uuid})
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
    return Response({'status': status, 'output': output, 'uuid': wav.uuid})


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
