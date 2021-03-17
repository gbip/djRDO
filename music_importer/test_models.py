from django.contrib.auth.models import User
from django.test import TestCase
import json

from music_importer.models import MusicTrack, Artist, Album


class MusicTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username="test_user", password="test_password")
        with open("music_importer/test_data/tracks.json") as file:
            tracks = json.load(file)
            for track in tracks:
                MusicTrack.objects.create_track(track, user)

    def test_data_is_present(self):
        track = MusicTrack.objects.get(title="L'aurore")
        assert track.bpm == 85
        assert track.title == "L'aurore"
