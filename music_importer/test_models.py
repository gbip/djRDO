from django.contrib.auth.models import User
from django.test import TestCase
import json

from music import key
from music_importer.models import MusicTrack, Artist, Album


class MusicTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username="test_user", password="test_password")
        with open("music_importer/test_data/tracks.json") as file:
            tracks = json.load(file)
            for track in tracks:
                # Convert camelot key to open key since we are not going through the form validation
                track["key"] = key.camelotToOpenKey[key.CamelotKey(track["key"])]
                MusicTrack.objects.create_track(track, user)

    def test_data_is_present(self):
        track = MusicTrack.objects.get(title="L'aurore")
        self.assertEqual(track.bpm, 85, "Invalid bpm : %r" % track.bpm)
        self.assertEqual(
            track.title, "L'aurore", "Invalid track name : %r" % track.title
        )
        self.assertEqual(
            track.artist.name,
            "Chinese Man",
            ("Invalid artist name : %r" % track.artist.name),
        )
        self.assertEqual(
            track.album.name,
            "Shikantaza",
            ("Invalid album name : %r" % track.album.name),
        )
        self.assertEqual(
            track.album.artist.name,
            "Chinese Man",
            ("Invalide album artist name : %r" % track.album.artist.name),
        )
        key_value = key.OpenKey[track.key.split(".")[1]]
        self.assertEqual(
            key_value,
            key.camelotToOpenKey[key.CamelotKey.A8],
            ("Invalid track key : %r" % track.key),
        )
