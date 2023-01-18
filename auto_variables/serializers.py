from rest_framework import serializers
from auto_variables.models import ExcelFile
from django.core.files import File
from requests import get
from auto_variables.utils import AutoVariable


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
            'id', 'api_document_id', 'file_url', 'file', 'output_file', 'is_download', 'is_finished', 'data',
        )
        read_only_fields = ('id', 'file', 'output_file', 'is_download', 'is_finished')

    def create(self, validated_data):
        self.instance = ExcelFile.objects.create(**validated_data)
        # upload.delay(self.instance.id, self.instance.file_url)
        response = get(self.instance.file_url)
        with open(self.instance.file_url.split('/')[-1], 'wb') as file:
            file.write(response.content)
        with open(self.instance.file_url.split('/')[-1], 'rb') as file:
            output_file = File(file, name='output.xlsx')
            self.instance.file = output_file
            self.instance.is_download = True
            self.instance.save()

        infos = AutoVariable(self.instance.file).info_file()
        info_list = []
        for key, alias in infos.items():
            if alias:
                info_list.append({
                    'name': key,
                    'categorical': True,
                    'open_ended': False
                })
            else:
                info_list.append({
                    'name': key,
                    'categorical': False,
                    'open_ended': True
                })

        self.instance.data = info_list
        self.instance.save()
        return self.instance
