from auto_variables import serializers
from drf_spectacular.utils import extend_schema
from  rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView


class VariableFileUpload(APIView):
    serializer_class = serializers.VariableFileSerializer
    permission_classes = (IsAuthenticated,)

    @extend_schema(tags=['auto_variable - File'], request=serializer_class)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# asd = {
#         "document_id": 5,
#         "data": [
#             {
#                 "name": "Sütun adı 1",
#                 "categoric": True,
#                 "open_ended": True
#             },
#             {
#                 "name": "Sütun adı 2",
#                 "categoric": False,
#                 "open_ended": True
#             }
#         ]
#     }
