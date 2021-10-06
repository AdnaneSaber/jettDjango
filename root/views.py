from django.shortcuts import render

from wsgiref.util import FileWrapper
from django.http import Http404, HttpResponse, HttpResponseRedirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from root.models import Model
from root.serializers import ModelSerializer
from django.conf import settings
import os


class Model_view(APIView):
    def get(self, request):
        print(os.path.join(settings.BASE_DIR, "db.sqlite3"))
        model = Model.objects.first()
        serializer = ModelSerializer(model)
        return Response(serializer.data)


class Model_Json_Download(generics.ListAPIView):
    def get(self, request, id):
        if os.path.exists(os.path.join(
                settings.BASE_DIR, f"jsonDirectory/Model-{id}.json")):
            file_handle = os.path.join(
                settings.BASE_DIR, f"jsonDirectory/Model-{id}.json")
            document = open(file_handle, 'rb')
            response = HttpResponse(FileWrapper(
                document), content_type='application/msword')
            response[
                'Content-Disposition'] = f'attachment; filename="Model-{id}.json"'
        else:
            return Response({"reponse": "JSON with the requeted id wasn't found !"})
        return response
