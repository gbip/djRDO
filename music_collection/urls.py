from django.urls import path, re_path

from music_collection.views import MusicCollectionListView, delete_collection

app_name = "music_collection"

urlpatterns = [
    path("", MusicCollectionListView.as_view(), name="music_list"),
    re_path(
        r"(?P<order_by>(bpm)|(key)|(artist)|(album)|(title)|(import_date)|(date_released)|(genre))(?P<dir>(asc)|(desc))",
        MusicCollectionListView.as_view(),
    ),
    path("delete_collection", delete_collection, name="delete_collection"),
]
