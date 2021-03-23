import json

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from music import key
from music_importer.models import MusicTrack
from music_importer.serializer_w import MusicTrackSerializerW
from music_importer.tests import import_tracks_from_test_json


class MusicImporterViewTestCase(TestCase):
    tracks = []

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            username="test_user", password="test_password", email="nomail@nomail.com"
        )
        cls.user.set_password("test_password")
        cls.user.save()

        with open("music_importer/test_data/tracks.json", "rb") as file:
            cls.tracks = json.load(file)

    def setUp(self):
        logged_in = self.client.login(
            username=self.user.username, password="test_password"
        )
        self.assertTrue(logged_in)

    def test_login_only_upload(self):
        response = self.client.get(reverse("music_importer:index"))
        self.assertEqual(response.status_code, 200)

    def test_loading_one_track(self):
        url = reverse("music_importer:upload")
        # Data that will be sent to the API
        post_data = [self.tracks[0]]

        # Data that will be used to compare the stored data with
        data = self.tracks[0]
        data["user"] = self.user.pk
        ser = MusicTrackSerializerW(data=data)
        valid = ser.is_valid()
        print(ser.errors)
        self.assertTrue(valid)

        response = self.client.post(
            url, json.dumps(post_data), content_type="application/json"
        )
        ser.save()
        self.assertEqual(response.status_code, 302)

        # Retrieve objects and check for equality
        d = MusicTrack.objects.filter(title=ser.data["title"])
        self.assertEqual(d[0], d[1])
