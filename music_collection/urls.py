from django.urls import path, re_path

from music_collection.views import (
    MusicTrackListView,
    delete_collection,
    MusicCollectionListView,
    create_collection,
)

app_name = "music_collection"

urlpatterns = [
    path("", MusicTrackListView.as_view(), name="music_list"),
    re_path(
        r"(?P<order_by>(bpm)|(key)|(artist)|(album)|(title)|(import_date)|(date_released)|(genre))(?P<dir>(asc)|(desc))",
        MusicTrackListView.as_view(),
    ),
    path("collection", MusicCollectionListView.as_view(), name="music_collection"),
    path("collection/create", create_collection, name="create_collection"),
    path("delete_collection", delete_collection, name="delete_collection"),
]
