from rest_framework import serializers
from auto_variables.models import ExcelFile
from auto_variables.tasks import generate_download
from auto_variables.tasks import info_file


class VariableInfoSerializer(serializers.Serializer):
    name = serializers.CharField(allow_null=False, required=True)
    categorical = serializers.BooleanField(allow_null=False, required=True)
    open_ended = serializers.BooleanField(allow_null=False, required=True)
    numeric = serializers.BooleanField(allow_null=False, required=True)

    def create(self, validated_data):
        return VariableInfoSerializer(**validated_data)

    def update(self, instance, validated_data):
        return VariableInfoSerializer(**validated_data)


class VariableFileSerializer(serializers.ModelSerializer):
    data = VariableInfoSerializer(many=True, read_only=True)

    class Meta:
        model = ExcelFile
        fields = (
            'id', 'api_document_id', 'file_url', 'file', 'output_file', 'is_download', 'is_finished', 'data'
        )
        read_only_fields = ('id', 'file', 'output_file', 'is_download', 'is_finished')

    def create(self, validated_data):
        self.instance = ExcelFile.objects.create(**validated_data)
        generate_download(self.instance.id, self.instance.file_url)
        infos = info_file(self.instance.id)
        self.instance.data = infos
        return self.instance

