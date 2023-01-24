from auto_variables import serializers
from drf_spectacular.utils import extend_schema
from  rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import requests
from auto_variables.tasks import generate_download, info_file


class VariableFileUpload(APIView):
    permission_classes = (IsAuthenticated,)

    @extend_schema(tags=['auto_variable - File'])
    def post(self, request):
        limit = 5 * 1024 * 1024
        file_url = request.data['file_url']
        if int(requests.get(file_url).headers['Content-Length']) > limit:
            serializer = serializers.VariableFileSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            instance = serializer.save()
            generate_download.delay(instance)
            info_file.delay(instance)
            return Response({'info': 'İsteğiniz kuyruğa alındı.'}, status=status.HTTP_202_ACCEPTED)
        else:
            serializer = serializers.VariableFileSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            instance = serializer.save()
            generate_download(instance)
            infos = info_file(instance)
            context = {
                'api_document_id': instance.api_document_id,
                'queue': False,
                'data': infos
            }
            serializer = serializers.VariableResultSerializer(context)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class CategoricalVariable(APIView):
    serializer_class = serializers.CategoricalVariableSerializer
    permission_classes = (IsAuthenticated,)

    @extend_schema(tags=['auto_variable - Categorical'], request=serializer_class)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
