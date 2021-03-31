"""
Allows user to group music into a collection, giving a logical name to a set of tracks.
"""

from django.db import models

# Create your models here.
from djRDO import settings


class MusicCollection(models.Model):
    title = models.CharField(max_length=500)
    date_created = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
