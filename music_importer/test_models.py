from django.contrib.auth.models import User
from django.test import TestCase
import json

from django.utils.dateparse import parse_date

from music import key
from music_importer.models import MusicTrack, Artist, Album


class MusicTestCase(TestCase):
    tracks = []

    def setUp(self):
        user = User.objects.create(username="test_user", password="test_password")
        with open("music_importer/test_data/tracks.json") as file:
            tracks = json.load(file)
            for track in tracks:
                # Convert camelot key to open key since we are not going through the form validation
                if track.get("key") is not None:
                    track["key"] = key.camelotToOpenKey[key.CamelotKey(track["key"])]
                if track.get("year") is not None:
                    track["year"] = parse_date(track["year"])
                MusicTrack.objects.import_track(track, user)
                self.tracks.append(track)

    def test_count(self):
        self.assertEqual(len(self.tracks), MusicTrack.objects.count())

    def validate_data(self, test_case):

        # Fetch artist ID
        artist = test_case.get("artist")
        if artist is not None:
            artist = Artist.objects.get(name=artist)

        # Fetch album artist ID
        album_artist = test_case.get("album_artist")
        if album_artist is not None:
            album_artist = Artist.objects.get(name=album_artist)

        # Fetch album ID
        album = test_case.get("album")
        if album is not None:
            if album_artist is not None:
                album = Album.objects.get(name=album, artist=album_artist)
            else:
                album = Album.objects.get(name=album)

        print(str(test_case))
        track = MusicTrack.objects.get(
            title=test_case["title"],
            key=test_case.get("key"),
            album=album,
            artist=artist,
            bpm=test_case.get("bpm"),
            date_released=test_case.get("year"),
        )
        print(track.date_released)

    def test_null_field_handling(self):
        for track in self.tracks[1:-1]:
            self.validate_data(track)

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
        # FIXME : this should be handled at the model level... :/
        key_value = key.OpenKey[track.key.split(".")[1]]
        self.assertEqual(
            key_value,
            key.camelotToOpenKey[key.CamelotKey.A8],
            ("Invalid track key : %r" % track.key),
        )
