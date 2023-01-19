from auto_variables import serializers
from drf_spectacular.utils import extend_schema
from  rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from auto_variables.models import ExcelFile


class VariableFileUpload(APIView):
    serializer_class = serializers.VariableFileSerializer
    permission_classes = (IsAuthenticated,)

    @extend_schema(tags=['auto_variable - File'], request=serializer_class)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class VariableFileDetail(APIView):
    serializer_class = serializers.VariableFileSerializer
    permission_classes = (IsAuthenticated,)

    @extend_schema(tags=['auto_variable - File'], request=serializer_class)
    def get(self, request, *args, **kwargs):
        queryset = ExcelFile.objects.filter(pk=kwargs['pk'])
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
