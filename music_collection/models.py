"""
Allows user to group music into a collection, giving a logical name and an order to a set of tracks.
"""

from django.db import models

# Create your models here.
from djRDO import settings
from music.models import MusicTrackWithNumber, MusicTrack
from utils.cover import MusicSetSvgRenderer


class MusicCollectionManager(models.Manager):
    def add_track_to_collection(self, music_track, collection):
        """
        Add a music track to a collection, picking the first track number available
        :param music_track: MusicTrack to be added to the collection. It is not modified
        :param collection: The collection to which the music track should be added. It is not modified.
        :return A MusicTrackWithNumber that is already saved in the database
        """
        available_number = collection.tracks.order_by("number")
        track_numbers = map(lambda x: x.number, available_number.all())
        num = get_next_track_number(list(track_numbers))
        result = collection.tracks.create(track_ptr=music_track, number=num)
        result.save()
        return result

    def change_track_number(self, old_track_number, new_track_number, collection):
        track = MusicTrackWithNumber.objects.get(
            number=old_track_number, collection=collection
        )
        other_track = MusicTrackWithNumber.objects.get(
            number=new_track_number, collection=collection
        )
        other_track.number = old_track_number
        track.number = new_track_number
        other_track.save()
        track.save()

    def get_last_number(self):
        return


class MusicCollection(models.Model):
    title = models.CharField(max_length=500, null=False, blank=False)
    date_created = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    objects = models.Manager()
    track_number_manager = MusicCollectionManager()

    @property
    def sorted_track_set(self):
        return self.tracks.order_by("number")

    def to_svg(self):
        track_set = MusicTrack.objects.filter(
            collection__collection__exact=self
        ).order_by("collection__number")
        renderer = MusicSetSvgRenderer(track_set)
        return renderer.render(self.title)


def get_next_track_number(arr):
    """
    Return an available track number from an array of already existing track numbers
    :param arr: A sequence of strictly positive integer representing track numbers, sorted in ascending order
    :return: The smallest integer missing in this sequence, strictly positive
    """
    if len(arr) == 0:
        return 1
    elif arr[0] != 1:
        return 1
    else:
        for i, k in zip(arr, arr[1:]):
            if k - i > 1:
                return i + 1
        return arr[-1] + 1
