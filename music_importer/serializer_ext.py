"""
This module defines a writable json interface
"""
from rest_framework import serializers
from rest_framework.fields import CharField

from music_importer.models import MusicTrack, Album, Artist, KeyField


class ArtistSerializerExt(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ["name"]


class AlbumSerializerExt(serializers.ModelSerializer):
    artist = ArtistSerializerExt()

    class Meta:
        model = Album
        fields = ["name", "artist"]


class MusicSerializerExt(serializers.ModelSerializer):
    artist = ArtistSerializerExt()
    album = AlbumSerializerExt()
    key = CharField(
        validators=[KeyField.validate_key],
        max_length=3,
        min_length=2,
        required=False,
    )

    class Meta:
        model = MusicTrack
        fields = [
            "title",
            "key",
            "bpm",
            "artist",
            "album",
            "genre",
            "date_released",
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
            album_data = validated_data.pop("album")
            album_artist_data = album_data.get("artist")
            album_artist = None
            if album_artist_data is not None:
                album_artist, _ = Artist.objects.get_or_create(
                    **album_artist_data, user=user
                )
            album_data["artist"] = album_artist
            Album.objects.insert(user=user, **album_data)
            album, _ = Album.objects.get_or_create(**album_data, user=user)

        return MusicTrack.objects.create(album=album, artist=artist, **validated_data)


class MultipleMusicSerializerExt(serializers.Serializer):
    tracks = MusicSerializerExt(many=True)

    class Meta:
        fields = ["tracks"]
