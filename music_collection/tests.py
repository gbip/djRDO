from django.contrib.auth import get_user_model
from django.test import TestCase

# Create your tests here.
from django.urls import reverse

from music_importer.models import MusicTrack


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
