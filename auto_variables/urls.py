from django.urls import path
from auto_variables import views

urlpatterns = [
    path("file-upload/", views.VariableFileUpload.as_view(), name="file_upload"),
]
