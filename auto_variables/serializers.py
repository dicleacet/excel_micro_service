from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from auto_variables.models import ExcelFile
from auto_variables.utils import AutoVariable
from auto_variables.tasks import upload


class VariableFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExcelFile
        fields = ('id', 'api_document_id', 'file_url', 'file', 'output_file', 'is_download', 'is_finished')
        read_only_fields = ('id', 'file', 'output_file', 'is_download', 'is_finished')

    def create(self, validated_data):
        self.instance = ExcelFile.objects.create(**validated_data)
        return self.instance
