"""
Data model to represent arbitrary music tracks.
A music track is made of some metadata (title, bpm, key) along with some links to other music objects such as an album
or an artist.
Every music model is linked to a user.
"""
import json

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.timezone import now

from music import key
from django.utils.translation import gettext_lazy as _


class ArtistManager(models.Manager):
    def get_by_natural_key(self, name, user):
        return (self.get_or_create(name=name, user_id=user))[0]


class Artist(models.Model):
    """
    Artist model :
        * Name - String
        * User - Key to a User
    """

    name = models.CharField(max_length=5000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    objects = ArtistManager()

    class Meta:
        unique_together = ["name", "user"]

    def natural_key(self):
        return self.name, self.user.pk

    def __str__(self):
        return self.name


class AlbumManager(models.Manager):
    def get_by_natural_key(self, name, artist, user):
        return (self.get_or_create(name=name, user_id=user, artist__name=artist))[0]


class Album(models.Model):
    """
    Album model :
        * Name - String
        * Artist - Key to an Artist
        * User - Key to a User
    """

    name = models.CharField(max_length=5000)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)

    objects = AlbumManager()

    class Meta:
        unique_together = ["name", "artist", "user"]

    def natural_key(self):
        return self.name, self.artist.natural_key(), self.user.pk

    natural_key.dependencies = ["music_importer.artist"]

    def __str__(self):
        return self.name


class MusicManager(models.Manager):
    @staticmethod
    def _normalize_json(track, user, album_name_list):
        user_key = user.pk
        track_fields = dict()
        album_fields = dict()

        track_fields["title"] = track["title"]
        track_fields["bpm"] = track.get("bpm")
        track_fields["key"] = track.get("key")
        track_fields["date_released"] = track.get("year")
        track_fields["genre"] = track.get("genre")
        track_fields["user"] = user_key

        # Handle album deferred creating
        if track.get("album") is not None:
            if track.get("album") not in album_name_list:
                # Instantiate an album
                album_fields["name"] = track.get("album")
                artist = track.get("album_artist") or track.get("artist")
                album_fields["artist"] = [artist, user_key]
                album_fields["user"] = user_key

            # Populate track fields
            track_fields["album"] = [
                track.get("album"),
                track.get("album_artist"),
                user_key,
            ]

        if track.get("artist") is not None:
            track_fields["artist"] = [track.get("artist"), user_key]

        model = (
            {"model": "music_importer.musictrack", "fields": track_fields},
            {"model": "music_importer.album", "fields": album_fields},
        )
        return model

    @staticmethod
    def normalize_tracks_to_json(tracks, user):
        """
        Normalize an array of track json to a single json object deserializable through django deserialization module
        See MusicManager.normalize_track_json for more information the json format expected.

        :return: A json array representing the django-deserializable version of the input data.
        """
        arr = []
        album_name_list = []
        for track in tracks:
            track_json, album_json = MusicManager._normalize_json(
                track, user, album_name_list
            )
            if album_json["fields"]:  # dict not empty
                album_name_list.append(album_json["fields"]["name"])
                arr.append(album_json)
            arr.append(track_json)

        return json.dumps(arr)

    @staticmethod
    def normalize_track_to_json(track, user):
        """
        Normalize a json so that it can be loaded through django deserialization module.

        :param track: Json data that represents a track. The only mandatory field is 'title'.

        :param user: The user that the track is linked to. This input should not be controlled by an end user and
            adequate verification should be performed.

        :return: A json string representing the track in django deserialization format.
        """

        result = MusicManager._normalize_json(track, user)
        return json.dumps(result)


def key_validator(val):
    """
    Validates that a key is either in the OpenKey format, the Camelot key format or the
    standard music key format
    :param val: The key to be validated
    """
    if val not in key.OpenKey.value:
        raise ValidationError(
            _(
                "%(value)s is not a valid music key. Expected a value such as 12m, 9A or 3d "
                "(camelot or openkey notation)."
            ),
            code="invalid",
            params={"value": val},
        )


class MusicTrack(models.Model):
    """
    Music model :
        * Title REQUIRED - String
        * Import date REQUIRED - DateTime
        * Bpm (optional)- Integer > 0
        * Album (optional) - Key to an Album
        * Artist (optional) - Key to an Artist
        * Key (optional) - Enum from key.OpenKey
        * Date Release (optional) - DateField
        * User REQUIRED - Key to a user
    """

    title = models.CharField(
        max_length=5000,
    )
    # Use default = now because auto_now_add fails when saving a DeserializedObject
    import_date = models.DateTimeField(default=now)
    bpm = models.PositiveSmallIntegerField(null=True, blank=True)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, null=True, blank=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, null=True, blank=True)
    key = models.CharField(
        max_length=3,
        choices=[(tag, tag.value) for tag in key.OpenKey],
        validators=[key_validator],
        null=True,
        blank=True,
    )
    date_released = models.DateField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    genre = models.CharField(max_length=200, null=True, blank=True)

    objects = MusicManager()

    def __str__(self):
        return "{0}".format(self.title)
