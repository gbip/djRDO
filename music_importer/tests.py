import json

from music_importer.models import Artist, Album
from music_importer.serializer_ext import MusicSerializerExt


# Create your tests here.


def import_tracks_from_test_json(path, l, user):
    """
    Import music tracks from test_data/tracks.json into the django database

    :param l: A lambda function to be called on each track
    :param user: The user associated with each track
    :return: Nothing
    """
    with open(path, "rb") as file:
        tracks = json.load(file)
        for track in tracks:
            l(track)

            serializer = MusicSerializerExt(data=track)
            serializer.initial_data["user"] = user.pk
            serializer.is_valid(raise_exception=True)
            serializer.save()

        print("Objects : ")
        print("\t Artists :" + str(Artist.objects.all()))
        print("\t Album :" + str(Album.objects.all()))
