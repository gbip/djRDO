from django.urls import path

from music_collection.views import MusicCollectionListView

app_name = "music_collection"

urlpatterns = [path("", MusicCollectionListView.as_view(), name="music_list")]
