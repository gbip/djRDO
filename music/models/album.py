from django.db import models

from djRDO import settings
from music.models.artist import Artist
from utils.cover import music_set_to_svg


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

    def to_svg(self):
        result = music_set_to_svg(self.musictrack_set, self.user.name + "_" + self.name)
        result.append(
            result.text(self.name + " by " + self.artist.name, x=8, y=0, fill="blue")
        )
        return result
