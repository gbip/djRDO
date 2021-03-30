from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from django.utils.datetime_safe import datetime

from music import key
from music_importer.models import MusicTrack, Artist, Album


class TestMultipleUserMusic(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = get_user_model().objects.create(
            username="user1", password="test_password", email="toto@toto.com"
        )
        cls.user1.set_password("test_password")
        cls.user1.save()
        cls.user2 = get_user_model().objects.create(
            username="user2", password="test_password", email="toto2@toto.com"
        )
        cls.user2.set_password("test_password")
        cls.user2.save()

    def test_no_data_sharing(self):
        music = MusicTrack(title="User1 music", user=self.user1)
        music.save()

        # Login with user1
        logged_in = self.client.login(
            username=self.user1.username, password="test_password"
        )
        self.assertTrue(logged_in)
        response = self.client.get(reverse("music_collection:music_list"))
        # Verify that we can see our music
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, music.title)

        # Login with client 2
        logged_in = self.client.login(
            username=self.user2.username, password="test_password"
        )
        self.assertTrue(logged_in)
        response = self.client.get(reverse("music_collection:music_list"))
        # Verify that we can see our music
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, music.title)


class TestOrdering(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create(
            username="user", password="test_password", email="toto@toto.com"
        )
        cls.user.set_password("test_password")
        cls.user.save()

    def ordering_test_helper(self, track_first, track_second, field_name):
        response = self.client.get(
            reverse("music_collection:music_list")
            + "?order_by="
            + field_name
            + "&dir=asc"
        )
        self.assertEqual(response.context["object_list"][0].pk, track_first.pk)
        self.assertEqual(response.context["object_list"][1].pk, track_second.pk)

        response = self.client.get(
            reverse("music_collection:music_list")
            + "?order_by="
            + field_name
            + "&dir=desc"
        )

        self.assertEqual(response.context["object_list"][1].pk, track_first.pk)
        self.assertEqual(response.context["object_list"][0].pk, track_second.pk)

    def test_ordering(self):
        self.assertTrue(
            self.client.login(username=self.user.username, password="test_password")
        )
        artist_first = Artist(name="A", user=self.user)
        artist_first.save()
        album_first = Album(name="A", artist=artist_first, user=self.user)
        album_first.save()
        track_first = MusicTrack(
            title="First",
            album=album_first,
            artist=artist_first,
            bpm=50,
            date_released=datetime.today() - timedelta(1),
            key=key.OpenKey.M1,
            user=self.user,
        )
        track_first.save()

        artist_second = Artist(name="B", user=self.user)
        artist_second.save()
        album_second = Album(name="B", artist=artist_second, user=self.user)
        album_second.save()

        track_second = MusicTrack(
            title="Second",
            album=album_second,
            artist=artist_second,
            bpm=51,
            date_released=datetime.now(),
            key=key.OpenKey.M2,
            user=self.user,
        )
        track_second.save()

        self.ordering_test_helper(track_first, track_second, "title")
        self.ordering_test_helper(track_first, track_second, "album")
        self.ordering_test_helper(track_first, track_second, "artist")
        self.ordering_test_helper(track_first, track_second, "bpm")
        self.ordering_test_helper(track_first, track_second, "key")
        self.ordering_test_helper(track_first, track_second, "import_date")
        self.ordering_test_helper(track_first, track_second, "date_released")
