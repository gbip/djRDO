import json

from django.core import serializers

# Create your tests here.
from music import key
from music_importer.models import MusicTrack


def import_tracks_from_test_json(l, user):
    """
    Import music tracks from test_data/tracks.json into the django database

    :param l: A lambda function to be called on each track
    :param user: The user associated with each track
    :return: Nothing
    """
    with open("music_importer/test_data/tracks.json") as file:
        tracks = json.load(file)
        for track in tracks:
            # Process tracks to parse the key from Camelot Key to open key
            if track.get("key") is not None:
                track["key"] = key.camelotToOpenKey[key.CamelotKey(track["key"])]

            if l is not None:
                l(track)

        data = MusicTrack.objects.normalize_tracks_to_json(tracks, user)
        objs_with_deferred_fields = []
        for obj in serializers.deserialize(
            "json",
            data,
            handle_forward_references=True,
        ):
            obj.save()
            if obj.deferred_fields is not None:
                objs_with_deferred_fields.append(obj)

        for obj in objs_with_deferred_fields:
            obj.save_deferred_fields()
