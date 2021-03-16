from django.urls import path

from . import views

app_name = "music_importer"

urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('upload', views.upload, name="upload")
]
