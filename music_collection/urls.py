from django.urls import path, re_path

from music_collection.views import (
    MusicTrackListView,
    MusicCollectionListView,
    MusicCollectionDetailView,
)

import music_collection.views as views

app_name = "music_collection"

urlpatterns = [
    path("", MusicTrackListView.as_view(), name="music_list"),
    re_path(
        r"(?P<order_by>(bpm)|(key)|(artist)|(album)|(title)|(import_date)|(date_released)|(genre))(?P<dir>(asc)|(desc))",
        MusicTrackListView.as_view(),
    ),
    path("collection", MusicCollectionListView.as_view(), name="collection_list"),
    path("collection/create", views.create_collection, name="create_collection"),
    path("delete_collection", views.delete_all_user_tracks, name="delete_collection"),
    path(
        "collection/<int:pk>/",
        MusicCollectionDetailView.as_view(),
        name="collection_detail",
    ),
    path("collection/remove_track", views.remove_track, name="collection_remove_track"),
    path(
        "collection/add_music",
        views.add_music_to_collection,
        name="add_music_to_collection",
    ),
    path("album/<int:pk>/cover", views.get_album_cover, name="album_cover"),
    path(
        "collection/<int:pk>/cover.svg",
        views.get_collection_cover,
        name="collection_cover_svg",
    ),
    path(
        "collection/<int:pk>/cover.pdf",
        views.get_collection_cover_pdf,
        name="collection_cover_pdf",
    ),
]
