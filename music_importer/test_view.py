import json

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from music import key
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
        response = self.client.post(
            url, self.tracks[0], content_type="application/json"
        )
        print(response.status_code)
        self.assertEqual(response.status_code, 200)
