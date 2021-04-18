from django.urls import path, re_path

from music_collection.views import (
    MusicTrackListView,
    delete_all_user_tracks,
    MusicCollectionListView,
    create_collection,
    MusicCollectionDetailView,
    add_music_to_collection,
    remove_track,
    get_album_cover,
    get_collection_cover,
)

app_name = "music_collection"

urlpatterns = [
    path("", MusicTrackListView.as_view(), name="music_list"),
    re_path(
        r"(?P<order_by>(bpm)|(key)|(artist)|(album)|(title)|(import_date)|(date_released)|(genre))(?P<dir>(asc)|(desc))",
        MusicTrackListView.as_view(),
    ),
    path("collection", MusicCollectionListView.as_view(), name="collection_list"),
    path("collection/create", create_collection, name="create_collection"),
    path("delete_collection", delete_all_user_tracks, name="delete_collection"),
    path(
        "collection/<int:pk>/",
        MusicCollectionDetailView.as_view(),
        name="collection_detail",
    ),
    path("collection/remove_track", remove_track, name="collection_remove_track"),
    path(
        "collection/add_music",
        add_music_to_collection,
        name="add_music_to_collection",
    ),
    path("album/<int:pk>/cover", get_album_cover, name="album_cover"),
    path(
        "collection/<int:pk>/cover.svg", get_collection_cover, name="collection_cover"
    ),
]
