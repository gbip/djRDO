import json

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from music import key


class MusicImporterViewTestCase(TestCase):
    tracks = []

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            username="test_user", password="test_password", email="nomail@nomail.com"
        )
        cls.client = Client()
        cls.client.login(username=user.username, password=user.password)
        with open("music_importer/test_data/tracks.json") as file:
            tracks = json.load(file)
            for track in tracks:
                # Convert camelot key to open key since we are not going through the form validation
                if track.get("key") is not None:
                    track["key"] = key.camelotToOpenKey[key.CamelotKey(track["key"])]
                if track.get("year") is not None:
                    # Modify year to only provide a year value since most music tags do not provide an exact date
                    track["year"] = track["year"][:4]
                cls.tracks.append(track)

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
