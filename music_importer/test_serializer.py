import json

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.exceptions import ErrorDetail

from music_importer.models import Album, MusicTrack
from music_importer.serializer_w import MusicTrackSerializerW


class MusicImporterSerializerSpecialBehaviourTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username="test_user", password="test_password")

    def test_simple_track(self):
        """
        Tries to load a simple track with just a title
        """
        with open("music_importer/test_data/simple_track.json", "rb") as file:
            tracks = json.load(file)
            self.assertEqual(len(tracks), 1)
            serializer = MusicTrackSerializerW(data=tracks[0])
            serializer.initial_data["user"] = self.user.pk
            valid = serializer.is_valid()
            self.assertTrue(valid)
            serializer.save()
            self.assertIsNotNone(MusicTrack.objects.get(title=tracks[0]["title"]))

    def test_album_creation(self):
        """
        Verify the behaviour when the an album is present multiple times with and without an artist field.
        At the end of the test, only one album should exist, with it's Artist field populated from the track data.
        :return:
        """
        files = [
            "music_importer/test_data/album_artist.json",
            "music_importer/test_data/album_artist_reversed.json",
        ]
        for file in files:
            self.generic_test_album_creation(file)

    def generic_test_album_creation(self, path):
        with open(path, "rb") as file:
            tracks = json.load(file)
            for track in tracks:
                serializer = MusicTrackSerializerW(data=track)
                serializer.initial_data["user"] = self.user.pk
                valid = serializer.is_valid()
                self.assertTrue(valid)
                serializer.save()
            album = Album.objects.get(name="Groovy psychology")
            self.assertEqual(album.artist.name, "Sigmund Freud")
            self.assertEqual(Album.objects.count(), 1)


class MusicImporterSerializerFailsTestCase(TestCase):
    """
    Test that the serializer correctly validates the track data
    """

    json_files = [
        "music_importer/test_data/invalid_album_without_name.json",
        "music_importer/test_data/invalid_bpm.json",
        "music_importer/test_data/invalid_key.json",
        "music_importer/test_data/invalid_no_title.json",
    ]

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username="test_user", password="test_password")

    def verify_error(self, path, error):
        with open(path, "rb") as file:
            tracks = json.load(file)
            self.assertEqual(len(tracks), len(error))
            for (track, error) in zip(tracks, error):
                serializer = MusicTrackSerializerW(data=track)
                serializer.initial_data["user"] = self.user.pk
                valid = serializer.is_valid()
                self.assertFalse(valid)
                self.assertDictEqual(serializer.errors, error)

    def test_invalid_album_without_name(self):
        error = {
            "album": {
                "name": [ErrorDetail(string="This field is required.", code="required")]
            }
        }
        self.verify_error(
            "music_importer/test_data/invalid_album_without_name.json", [error]
        )

    def test_invalid_bpm(self):
        error = [
            {
                "bpm": [
                    ErrorDetail(string="A valid integer is required.", code="invalid")
                ]
            },
            {
                "bpm": [
                    ErrorDetail(
                        string="Ensure this value is greater than or equal to 0.",
                        code="min_value",
                    )
                ]
            },
        ]
        self.verify_error("music_importer/test_data/invalid_bpm.json", error)

    def test_invalid_key(self):
        error = [
            {"key": [ErrorDetail(string="Invalid music key : 13A", code="invalid")]},
            {"key": [ErrorDetail(string="Invalid music key : 37", code="invalid")]},
        ]
        self.verify_error("music_importer/test_data/invalid_key.json", error)

    def test_invalid_no_title(self):
        error = {
            "title": [ErrorDetail(string="This field is required.", code="required")]
        }
        self.verify_error("music_importer/test_data/invalid_no_title.json", [error])
