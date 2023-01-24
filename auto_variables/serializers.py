from rest_framework import serializers
from auto_variables.models import ExcelFile
from auto_variables.tasks import generate_download
from auto_variables.tasks import info_file
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


# class VariableFileSerializer(serializers.ModelSerializer):
#     data = VariableInfoSerializer(many=True, read_only=True)
#     queue = serializers.BooleanField(allow_null=False, read_only=True)
#
#     class Meta:
#         model = ExcelFile
#         fields = (
#             'id', 'api_document_id', 'data', 'queue'
#         )
#         read_only_fields = ('id',)
#
#     def create(self, validated_data):
#         self.instance = ExcelFile.objects.create(**validated_data, file_url=self.context['file_url'])
#         generate_download(self.instance)
#         infos = info_file(self.instance)
#         self.instance.queue = False
#         self.instance.data = infos
#         return self.instance


class VariableFileSerializer(serializers.Serializer):
    api_document_id = serializers.IntegerField(allow_null=False, required=True)
    file_url = serializers.URLField(allow_null=False, required=True)

    def create(self, validated_data):
        self.instance = ExcelFile.objects.create(**validated_data)
        return self.instance

    def update(self, instance, validated_data):
        return VariableFileSerializer(**validated_data)


class VariableResultSerializer(serializers.Serializer):
    data = VariableInfoSerializer(many=True, read_only=True)
    queue = serializers.BooleanField(allow_null=False, read_only=True)
    api_document_id = serializers.IntegerField(allow_null=False, read_only=True)

    def create(self, validated_data):
        return VariableResultSerializer(**validated_data)

    def update(self, instance, validated_data):
        return VariableResultSerializer(**validated_data)


















class CategoricalVariableSerializer(serializers.Serializer):
    data = VariableInfoSerializer(many=True, write_only=True, allow_null=False, required=True)
    id = serializers.IntegerField(allow_null=False, required=True)
    value_mean = serializers.CharField(read_only=True, allow_null=False)
    output_file = serializers.CharField(read_only=True, allow_null=False)

    def create(self, validated_data):
        self.instance = ExcelFile.objects.filter(id=validated_data['id']).first()
        data = validated_data.get('data')
        value_mean, file_path = AutoVariable(self.instance.file).split_data(data)
        self.instance.value_mean = value_mean
        self.instance.output_file = file_path
        self.instance.save()
        return self.instance

    def update(self, instance, validated_data):
        return CategoricalVariableSerializer(**validated_data)
