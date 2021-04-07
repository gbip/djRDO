"""
Data model to represent arbitrary music tracks.
A music track is made of some metadata (title, bpm, key) along with some links to other music objects such as an album
or an artist.
Every music model is linked to a user.
"""

from django.contrib.auth.models import User
from django.core import exceptions
from django.db import models
from django.utils.timezone import now

from djRDO import settings
from utils import key


class KeyField(models.CharField):
    """
    Implement a field that only holds value that represents valid music key.
    """

    description = "A music key"

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 3
        super().__init__(*args, **kwargs)
        self.key = None

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs["max_length"]
        return name, path, args, kwargs

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return KeyField.validate_key(value)

    @classmethod
    def validate_key(cls, value):
        """
        Validates the key by trying to find it in the 3 supported music notation
        """
        if value is None:
            return None
        elif value in set(k.value for k in key.OpenKey):
            return value
        elif value in set(k.value for k in key.CamelotKey):
            return key.camelotKeyToOpenKey[key.CamelotKey(value)]
        elif value in set(k.value for k in key.MusicKey):
            return key.musicKeyToOpenKey[key.MusicKey(value)]
        else:
            raise exceptions.ValidationError("Invalid music key : {}".format(value))

    def to_python(self, value):
        if isinstance(value, key.OpenKey):
            return value
        if value is None:
            return value

        return KeyField.validate_key(value)

    def get_prep_value(self, value):
        return value

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return self.get_prep_value(value)


class Artist(models.Model):
    """
    Artist model :
        * Name - String
        * User - Key to a User
    """

    name = models.CharField(max_length=5000)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Album(models.Model):
    """
    Album model :
        * Name - String
        * Artist - Key to an Artist
        * User - Key to a User
    """

    name = models.CharField(max_length=5000)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False
    )

    def __str__(self):
        return (
            self.name
            + " - "
            + str(self.artist.name if self.artist is not None else None)
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
        * Collections (optional) - M2M to a collection
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
    key = KeyField(
        null=True,
        blank=True,
    )
    date_released = models.DateField(null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    genre = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return "{0}".format(self.title)

    def __eq__(self, other):
        return (
            self.bpm == other.bpm
            and self.key == other.key
            and self.title == other.title
            and self.genre == other.genre
            and self.date_released == other.date_released
            and self.artist == other.artist
            and self.album == other.album
        )

    def __hash__(self):
        return hash(self.id)

    def get_key_color(self):
        if self.key is None:
            return "000000"
        else:
            return key.openKeyColors[self.key]


class MusicTrackWithNumber(models.Model):
    """
    Link a music track to a collection, adding a number to the track.
    This allow tracks to be ordered in a collection.
    """

    number = models.PositiveSmallIntegerField()
    track_ptr = models.OneToOneField(
        MusicTrack, on_delete=models.CASCADE, related_name="collection"
    )
    collection = models.ForeignKey(
        "music_collection.MusicCollection",
        on_delete=models.CASCADE,
        related_name="tracks",
    )

    class Meta:
        ordering = ["number"]
