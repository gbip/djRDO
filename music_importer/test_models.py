from django.contrib.auth.models import User
from django.core import serializers
from django.test import TestCase
import json

from django.utils.dateparse import parse_date

from music import key
from music_importer.models import MusicTrack, Artist, Album


class MusicImporterSerializerTestCase(TestCase):
    def test_natural_key_creation(self):
        user = User.objects.create(username="test_user", password="test_password")
        with open("music_importer/test_data/tracks.json") as file:
            tracks = json.load(file)
            track = tracks[0]  # "L'aurore"
            if track.get("key") is not None:
                track["key"] = key.camelotToOpenKey[key.CamelotKey(track["key"])]
            data = MusicTrack.objects.normalize_tracks_json([track], user)
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

        self.assertEqual(
            track.key,
            key.camelotToOpenKey[key.CamelotKey.A8],
            ("Invalid track key : %r" % track.key),
        )


class MusicImporterModelTestCase(TestCase):
    tracks = []
    user = None

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username="test_user", password="test_password")
        with open("music_importer/test_data/tracks.json") as file:
            tracks = json.load(file)
            for track in tracks:
                # Convert camelot key to open key since we are not going through the form validation
                if track.get("key") is not None:
                    track["key"] = key.camelotToOpenKey[key.CamelotKey(track["key"])]
                # if track.get("year") is not None:
                #    track["year"] = parse_date(track["year"])
                cls.tracks.append(track)

        data = MusicTrack.objects.normalize_tracks_json(cls.tracks, cls.user)

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

        print(MusicTrack.objects.all())
        print(Album.objects.all())
        print(Artist.objects.all())

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
                album = Album.objects.get(
                    name=album, artist=album_artist, user=self.user
                )
            else:
                album = Album.objects.get(name=album, artist=None, user=self.user)

        track = MusicTrack.objects.get(
            title=test_case["title"],
            key=test_case.get("key"),
            album=album,
            artist=artist,
            bpm=test_case.get("bpm"),
            date_released=test_case.get("year"),
        )

        self.assertIsNotNone(track)

    def test_null_field_handling(self):
        for track in self.tracks[1:-1]:
            self.validate_data(track)
