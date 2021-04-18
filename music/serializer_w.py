"""
This module defines a writable json interface that allows to serialize a track that embeds an artist and an album field.
"""
from rest_framework import serializers
from rest_framework.fields import CharField, IntegerField, DateField

from music.models import MusicTrack, Album, Artist, KeyField


class ArtistSerializerW(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ["name"]


class AlbumSerializerW(serializers.ModelSerializer):
    artist = ArtistSerializerW(required=False)

    class Meta:
        model = Album
        fields = ["name", "artist"]


class MusicTrackSerializerW(serializers.ModelSerializer):
    """
    This serializer is responsible for writing tracks to the database. It supports album and artist fields.
    Upon track creation, if an artist field is present, and it is missing from the database then such an artist will be
    created.
    For an album the logic is a little bit more complicated.
    Then we use the of Album.update_or_create(), that handles :
    1) If the same album exist without an artist, then add the artist to the album
    2) If the same album exist with an artist while we don't provide one, then use this album
    3) If the album does simply not exist, create it
    """

    artist = ArtistSerializerW(required=False)
    album = AlbumSerializerW(required=False)
    bpm = IntegerField(min_value=0, required=False)
    key = CharField(
        validators=[KeyField.validate_key], max_length=3, min_length=2, required=False
    )
    year = DateField(source="date_released", required=False, input_formats=["%Y", "Y"])

    class Meta:
        model = MusicTrack
        fields = [
            "title",
            "key",
            "bpm",
            "artist",
            "album",
            "genre",
            "year",
            "user",
        ]

    def create(self, validated_data):
        user = validated_data.get("user")

        artist = None
        if validated_data.get("artist"):
            artist_data = validated_data.pop("artist")
            artist, _ = Artist.objects.get_or_create(**artist_data, user=user)

        album = None
        if validated_data.get("album"):
            # Dict passed to update_or_create holding the new values for the album
            defaults = {}
            album_data = validated_data.pop("album")
            album_artist_data = album_data.get("artist")
            if album_artist_data is not None:
                album_artist, _ = Artist.objects.get_or_create(
                    **album_artist_data, user=user
                )
                # We don't want to remove an existing artist !!!
                defaults["artist"] = album_artist
                # This is needed so that the ORM can find the album
                album_data["artist"] = album_artist

            defaults["name"] = album_data.get("name")
            album, p = Album.objects.update_or_create(
                user=user, **album_data, defaults=defaults
            )

        return MusicTrack.objects.create(album=album, artist=artist, **validated_data)
