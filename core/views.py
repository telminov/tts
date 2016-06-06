from django.shortcuts import render

# Create your views here.
from core.models import SomeModel
from core.serializers import SomeModelSerializer
from django.http import Http404, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status




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