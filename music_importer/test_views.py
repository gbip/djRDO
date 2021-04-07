import json

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from music_importer.models import MusicTrack
from music_importer.serializer_w import MusicTrackSerializerW
from utils.test import DjRDOTestHelper


class MusicImporterViewTestCase(DjRDOTestHelper):
    """
    Test that the upload view correctly works
    """

    tracks = []

    @classmethod
    def setUpTestData(cls):
        super(MusicImporterViewTestCase, cls).setUpTestData()
        with open("music_importer/test_data/tracks.json", "rb") as file:
            cls.tracks = json.load(file)

    def setUp(self):
        self.login("user")

    def test_upload_permissions(self):
        client = Client()

        # /index, not logged in
        response = client.get(reverse("music_importer:index"))
        redirect_url = (
            reverse("accounts:login") + "?next=" + reverse("music_importer:index")
        )
        self.assertRedirects(response, redirect_url)

        # /index, logged in
        response = self.client.get(reverse("music_importer:index"))
        self.assertEqual(response.status_code, 200)

        # /upload not logged in
        response = client.get(reverse("music_importer:upload"))
        redirect_url = (
            reverse("accounts:login") + "?next=" + reverse("music_importer:upload")
        )
        self.assertRedirects(response, redirect_url)

    def test_loading_one_track(self):
        """
        Load a single track and verify it's value
        """
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
        self.assertEqual(response.status_code, 200)

        # Retrieve objects and check for equality
        d = MusicTrack.objects.filter(title=ser.data["title"])
        self.assertEqual(d[0], d[1])
        self.assertEqual(MusicTrack.objects.count(), 2)

    def test_loading_all_tracks(self):
        url = reverse("music_importer:upload")
        response = self.client.post(
            url, json.dumps(self.tracks), content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(MusicTrack.objects.count(), len(self.tracks))
