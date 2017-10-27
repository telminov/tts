from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response

from django.urls import reverse_lazy
from django.views.generic import RedirectView

from core import models
from core import serializers
from core.generic.mixins import ResponseSerializerMixin


class Index(RedirectView):
    url = reverse_lazy('api-docs:docs-index')


class Generate(ResponseSerializerMixin, generics.CreateAPIView):
    serializer_class = serializers.Generate
    response_serializer_class = serializers.Voice

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        returncode, instance = serializer.save()

        if returncode == 0 and instance:
            serializer = self.get_response_serializer(instance=instance)
            response = Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            response = Response(data=dict(rhvoice_returncode=returncode), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return response


class Speech(generics.RetrieveAPIView):
    queryset = models.Speech.objects.all()
    lookup_field = 'uuid'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = serializers.Voice(instance=instance, context=dict(request=request))

        return Response(data=serializer.data, status=status.HTTP_200_OK)
