# Create your views here.
import subprocess
import os

from django.http import Http404, JsonResponse
from django.http import HttpResponse
from django.conf import settings
from django.core.files import File

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core.models import SomeModel, Wav
from core.serializers import SomeModelSerializer

class SomeModelList(APIView):
    """Список объектов SomeModel
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

def generate_speach(request, text):
    wav = Wav(text=text)
    file_out = '%s.wav' % wav.uuid
    command = 'echo %s | RHVoice-test -p irina -o %s' % (text, file_out)
    wav.command = command
    status, output = subprocess.getstatusoutput(command)
    path_to_file = os.path.join(settings.BASE_DIR, file_out)
    f = open(path_to_file, "rb")
    wav.file = File(f)
    wav.save()
    return JsonResponse({'status': status, 'output': output, 'uuid': wav.uuid})

def play_speach(request, uuid):
    wavs = Wav.objects.filter(uuid=uuid)
    if wavs:
        f = wavs.first().file
        response = HttpResponse()
        response.write(f.file.read())
        response['Content-Type'] = 'audio/mp3'
        response['Content-Length'] = os.path.getsize(f.path)
        return response
    else:
        raise Http404(u'Нет такого файла')