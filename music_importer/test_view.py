from django.contrib.auth.models import User
from django.core import serializers
from django.http import HttpResponseRedirect
from django.test import TestCase, Client
from django.urls import reverse
import json

from django.utils.dateparse import parse_date

from music import key
from music_importer.models import MusicTrack, Artist, Album


class MusicImporterViewTestCase(TestCase):
    tracks = []

    def setUp(self):
        user = User.objects.create_user(
            username="test_user", password="test_password", email="nomail@nomail.com"
        )
        self.client = Client()
        self.client.login(username="test_user", password="test_password")
        with open("music_importer/test_data/tracks.json") as file:
            tracks = json.load(file)
            for track in tracks:
                # Convert camelot key to open key since we are not going through the form validation
                if track.get("key") is not None:
                    track["key"] = key.camelotToOpenKey[key.CamelotKey(track["key"])]
                if track.get("year") is not None:
                    # Modify year to only provide a year value since most music tags do not provide an exact date
                    track["year"] = track["year"][:4]
                self.tracks.append(track)

    def test_login_only_upload(self):
        response = self.client.get(reverse("music_importer:index"))
        self.assertEqual(response.status_code, 200)

    def test_loading_one_track(self):
        url = reverse("music_importer:upload")
        response = self.client.post(
            url, self.tracks[0], content_type="application/json"
        )
        print(response.status_code)
