import subprocess

from rest_framework import status
from rest_framework import views
from rest_framework import generics
from rest_framework.response import Response

from django.core.files.uploadedfile import TemporaryUploadedFile
from django.views.generic import RedirectView
from django.urls import reverse_lazy

from core import models
from core import serializers


class Index(RedirectView):
    url = reverse_lazy('')


class Generate(generics.CreateAPIView):
    serializer_class = serializers.Generate

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        voice = serializer.validated_data['voice']
        text = serializer.validated_data['text']

        with TemporaryUploadedFile(None, None, None, None) as temp:
            echo = subprocess.Popen(['echo', text], stdout=subprocess.PIPE)
            rhv = subprocess.Popen(['RHVoice-test', '-p', voice, '-o', temp.temporary_file_path()], stdin=echo.stdout)

            if echo.wait() == 0 and rhv.wait() == 0:
                serializer = serializers.Voice(instance=models.Voice.objects.create(text=text, file=temp))
                response = Response(
                    data=serializer.data,
                    status=status.HTTP_201_CREATED
                )
            else:
                response = Response(
                    data=dict(rhvoice_returncode=rhv.returncode),
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        return response

# @api_view(['post'])
# def generate(request):
#     """
#     ---
#     parameters:
#     - name: text
#       description: Text for generation
#       required: true
#       paramType: form
#     """
#     serializer = serializers.Generatу(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     text = serializer.validated_data['text']
#
#
#
#     file_uuid = uuid.uuid4()
#     tmp_path = '{}/{}.wav' % (tmp_dir, file_uuid)
#
#     file_path = os.path.join(tempfile.gettempdir(), )
#
#
#     command = 'echo %s | RHVoice-test -p elena -o %s' % (text, tmp_path)
#     status_code, output = subprocess.getstatusoutput(command)
#     if status_code != 0:
#         return Response(
#             {'error': 'File generation error', 'output': output},
#             status=status.HTTP_500_INTERNAL_SERVER_ERROR
#         )
#
#     with open(tmp_path, 'rb') as tmp_file:
#         models.SoundFile.objects.create(
#             uuid=file_uuid,
#             text=text,
#             command=command,
#             file=File(tmp_file),
#             type='wav',
#         )
#
#     os.unlink(tmp_path)
#     return JsonResponse({'status': status_code, 'uuid': file_uuid})


# @api_view()
# def get_file(request):
#     """
#     ---
#     parameters:
#     - name: uuid
#       description: uuid of generated file
#       required: true
#       paramType: query
#     """
#     serializer = serializers.GetFile(data=request.query_params)
#     serializer.is_valid(raise_exception=True)
#
#     sound_file = models.SoundFile.objects.get(uuid=serializer.validated_data['uuid'])
#
#     response = HttpResponse()
#     response.write(sound_file.file.read())
#
#     response['Content-Type'] = 'audio/vnd.wave'
#     response['Content-Length'] = sound_file.file.size
#     response['Content-Disposition'] = 'attachment; filename=%s' % sound_file.file.name.split('/')[-1]
#
#     return response
