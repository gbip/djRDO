from django.urls import path

from . import views

app_name = "music"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("upload", views.upload, name="upload"),
    path("albums", views.AlbumListView.as_view(), name="albums"),
    path("album/<int:pk>", views.AlbumDetailView.as_view(), name="album_detail_view"),
    path("album/<int:pk>/cover", views.get_album_generated_cover, name="album_cover"),
]
