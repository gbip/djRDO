"""
Data model to represent arbitrary music tracks.
A music track is made of some metadata (title, bpm, key) along with some links to other music objects such as an album
or an artist.
Every music model is linked to a user.
"""
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import MinValueValidator
from music import key
from django.utils.translation import gettext_lazy as _


# Create your models here.


class Artist(models.Model):
    """
    Artist model :
        * Name - String
        * User - Key to a User
    """

    name = models.CharField(max_length=5000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Album(models.Model):
    """
    Album model :
        * Name - String
        * Artist - Key to an Artist
        * User - Key to a User
    """

    name = models.CharField(max_length=5000)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class MusicManager(models.Manager):
    def import_track(self, track, user):
        """
        Import a track, handling null fields as needed
        :param track: python dictionary representing a track
        :param user: user that will be the owner of the track and all objects created for its representation (album, artist)
        """
        # Try to import foreign keys. First check if the foreign key field is present in the provided data
        #
        # album : first check for the album artist, then for the album
        album_artist = track.get("album_artist")
        if album_artist is not None:
            album_artist, _ = Artist.objects.get_or_create(
                name=track["album_artist"], user=user
            )
            album_artist.save()

        album = track.get("album")
        if album is not None:
            if album_artist is not None:
                album, _ = Album.objects.get_or_create(
                    name=track["album"], artist=album_artist, user=user
                )
                album.save()
            else:
                album, _ = Album.objects.get_or_create(name=track["album"], user=user)
                album.save()

        artist = track.get("artist")
        if artist is not None:
            artist, _ = Artist.objects.get_or_create(name=track["artist"], user=user)
            artist.save()

        self.create_track(
            user=user,
            title=track["title"],
            artist=artist,
            album=album,
            bpm=track.get("bpm"),
            track_key=track.get("key"),
            date_released=track.get("year"),
        )

    def create_track(
        self,
        user,
        title,
        artist=None,
        album=None,
        bpm=None,
        track_key=None,
        date_released=None,
    ):
        """
        Insert a new track within the database
        :param date_released: Optional track release date
        :param track_key: Optional track key
        :param bpm: Optional track BPM
        :param album: Optional album id
        :param artist: Optional artist id
        :param title: Mandatory title string
        :param user: A django user to use as the owner of the track
        """
        # Create music
        music = self.create(
            title=title,
            bpm=bpm,
            artist=artist,
            album=album,
            key=track_key,
            date_released=date_released,
            user=user,
        )
        return music


def key_validator(val):
    """
    Validates that a key is either in the OpenKey format, the Camelot key format or the
    standard music key foramt
    :param val: The key to be validated
    """
    if not val in key.OpenKey.value:
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
    import_date = models.DateTimeField(auto_now_add=True)
    bpm = models.IntegerField(
        validators=[MinValueValidator(0, "Bpm must be positive")], null=True, blank=True
    )
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
