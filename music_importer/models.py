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
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class MusicManager(models.Manager):
    def create_track(self, track, user):
        """
        Insert a new track within the database
        :param track: A python dict describing a track
        :param user: A django user to use as the owner of the track, the album and the artist
        """
        # Create album artist
        album_artist, _ = Artist.objects.get_or_create(
            name=track["album_artist"], user=user
        )
        album_artist.save()

        # Create album
        album, _ = Album.objects.get_or_create(
            name=track["album"], artist=album_artist, user=user
        )
        album.save()

        # Create artist
        artist, _ = Artist.objects.get_or_create(name=track["artist"], user=user)
        artist.save()

        # Create music
        music = self.create(
            title=track["title"],
            bpm=track["bpm"],
            artist=artist,
            album=album,
            key=track["key"],
            date_released=track["year"],
            user=user,
        )
        return music


def key_validator(val):
    """
    Validates that a key is either in the OpenKey format, the Camelot key format or the
    standard music key foramt
    :param val: The key to be validated
    """
    if (
        not val in key.OpenKey.value
        and not val in key.MusicKey.value
        and not val in key.CamelotKey.value
    ):
        raise ValidationError(
            _("%(value)s is not a valid music key"),
            code="invalid",
            params={"value": val},
        )


class MusicTrack(models.Model):
    """
    Music model :
        * Title - String
        * Import date - DateTime
        * Bpm - Integer > 0
        * Album - Key to an Album
        * Artist - Key to an Artist
        * Key - Enum from key.OpenKey
        * Date Release - DateField
        * User - Key to a user
    """

    title = models.CharField(max_length=5000)
    import_date = models.DateTimeField(auto_now_add=True)
    bpm = models.IntegerField(validators=[MinValueValidator(0, "Bpm must be positive")])
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    key = models.CharField(
        max_length=3,
        choices=[(tag, tag.value) for tag in key.OpenKey],
        validators=[key_validator],
    )
    date_released = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    objects = MusicManager()
