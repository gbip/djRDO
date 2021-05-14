from django.db import models

from djRDO import settings
from music.models.artist import Artist
from utils.cover import MusicSetSvgRenderer


class UserAlbumManager(models.Manager):
    def get(self, user):
        return self.get_queryset().filter(user=user)


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

    objects = models.Manager()
    user_albums = UserAlbumManager()

    def __str__(self):
        return (
            self.name
            + " - "
            + str(self.artist.name if self.artist is not None else None)
        )

    def to_svg(self):
        renderer = MusicSetSvgRenderer(self.musictrack_set, font_size=16)
        result = renderer.render(self.name)

        return result
