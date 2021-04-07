import io

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils.datetime_safe import date, datetime
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from utils import key
from music_importer.models import MusicTrack, Artist, Album
from music_importer.serializer_w import MusicTrackSerializerW
from music_importer.tests import import_tracks_from_test_json


class MusicImporterSerializerTestCase(TestCase):
    """
    Test that the serializer is able to serialize/deserialize it's own data
    """

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create(
            username="test_user", password="test_password", email="toto@toto.com"
        )

    def test_track_serialization(self):
        """
        Tries to serialize then deserialized a track, and checks that it has not changed
        """
        artist = Artist(name="Potato musician", user=self.user)
        artist.save()
        album_artist = Artist(name="Creamy Cheese", user=self.user)
        album_artist.save()
        album = Album(name="Awesome album", artist=album_artist, user=self.user)
        album.save()

        track = MusicTrack(
            title="Tartiflette",
            bpm=250,
            genre="food",
            artist=artist,
            album=album,
            user=self.user,
            date_released=str(date.today().year),
            key="3d",
        )

        serializer = MusicTrackSerializerW(track)
        json = JSONRenderer().render(serializer.data)
        stream = io.BytesIO(json)
        data = JSONParser().parse(stream)
        serializer2 = MusicTrackSerializerW(data=data)
        serializer2.user = self.user
        self.assertTrue(serializer2.is_valid())
        serializer2.save()

        saved_track = MusicTrack.objects.get(title=track.title)
        track.key = key.OpenKey.D3
        saved_track.date_released = str(saved_track.date_released.year)
        self.assertEqual(saved_track, track)
        self.assertEqual(Album.objects.count(), 1)
        self.assertEqual(Artist.objects.count(), 2)


class MusicImporterModelTestCase(TestCase):
    """
    Test that we are able to import real track metadata
    """

    tracks = []
    user = None

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create(
            username="test_user", password="test_password"
        )
        import_tracks_from_test_json(
            "music_importer/test_data/tracks.json",
            lambda x: cls.tracks.append(x),
            cls.user,
        )

    def test_count(self):
        """
        Verify that we have the right number of album in our database
        """
        self.assertEqual(len(self.tracks), MusicTrack.objects.count())
        # Count the number of unique albums
        album_count = len(
            set(
                [
                    t.get("album").get("name")
                    for t in self.tracks
                    if t.get("album") is not None
                ]
            )
        )
        self.assertEqual(album_count, Album.objects.count())

    def validate_data(self, test_case):
        """
        Validate that the database data matches the track data

        :param test_case: a dict representing a track
        """
        # Fetch artist ID
        artist = test_case.get("artist")
        if artist is not None:
            artist = Artist.objects.get(name=artist["name"], user=self.user)

        # Fetch album artist ID
        album_artist = test_case.get("album_artist")
        if album_artist is not None:
            album_artist = Artist.objects.get(name=album_artist, user=self.user)

        # Fetch album ID
        album = test_case.get("album")
        if album is not None:
            if album_artist is not None:
                album = Album.objects.get(
                    name=album, artist=album_artist, user=self.user
                )
            else:
                album = Album.objects.get(name=album["name"], user=self.user)

        track = MusicTrack.objects.get(
            title=test_case["title"],
            key=test_case.get("key"),
            album=album,
            artist=artist,
            bpm=test_case.get("bpm"),
            date_released=datetime.strptime(test_case.get("year"), "%Y"),
        )
        self.assertIsNotNone(track)

    def validate_uniqueness(self, test_case):
        """
        Validate that we have the right amount of album in the database

        :param test_case: A dict representing a track
        """
        track = MusicTrack.objects.get(title=test_case["title"], user=self.user)
        self.assertIsNotNone(track)
        if test_case.get("album") is not None:
            try:
                album = Album.objects.get(
                    name=test_case["album"]["name"], user=self.user
                )
                self.assertIsNotNone(album)
            except:
                raise RuntimeError("Not unique")

    def test_all_track_import(self):
        """
        Verify that the database is in a state consistent with the collection of track loaded
        """
        for track in self.tracks[1:-1]:
            self.validate_data(track)
            self.validate_uniqueness(track)

    def test_simple_track(self):
        """
        Verify by hand that a track has been correctly imported
        """
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
            key.OpenKey.M1,
            ("Invalid track key : %r" % track.key),
        )
