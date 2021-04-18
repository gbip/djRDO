from django.db import models
from django.utils.timezone import now

from djRDO import settings
from music.models import Artist, Album, KeyField
from utils import key


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