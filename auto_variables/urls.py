from django.urls import path
from auto_variables import views

urlpatterns = [
    path("file-upload/", views.VariableFileUpload.as_view(), name="file_upload"),
    path("file-detail/<int:pk>/", views.VariableFileDetail.as_view(), name="file_detail")
]
