"""
This module holds common test code
"""
import json

from music_importer.serializer_w import MusicTrackSerializerW


# Create your tests here.


def import_tracks_from_test_json(path, l, user):
    """
    Import utils tracks from the provided path, and calls l on each track.

    :param path: A path to a json file representing the tracks to be loaded
    :param l: A lambda function to be called on each track
    :param user: The user associated with each track
    :return: Nothing
    """
    with open(path, "rb") as file:
        tracks = json.load(file)
        for track in tracks:
            if l is not None:
                l(track)

            print(track)
            serializer = MusicTrackSerializerW(data=track)
            serializer.initial_data["user"] = user.pk
            serializer.is_valid(raise_exception=True)
            serializer.save()
