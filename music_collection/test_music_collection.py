from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from music_collection.models import MusicCollection
from music_importer.models import MusicTrack


class TestMusicCollection(TestCase):
    """
    Test that multiple user can't see each other data
    """

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
        """
        Creates two user, with a single track each. Then tries to fetch the tracklist and make sure each user can only
        see their track
        """
        collection = MusicCollection(title="User1 music", user=self.user1)
        collection.save()

        # Login with user1
        logged_in = self.client.login(
            username=self.user1.username, password="test_password"
        )
        self.assertTrue(logged_in)
        response = self.client.get(reverse("music_collection:collection_list"))
        # Verify that we can see our music
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, collection.title)

        # Login with client 2
        logged_in = self.client.login(
            username=self.user2.username, password="test_password"
        )
        self.assertTrue(logged_in)
        response = self.client.get(reverse("music_collection:collection_list"))
        # Verify that we can see our music
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, collection.title)

    def test_same_name(self):

        collection = MusicCollection(title="name", user=self.user1)
        music1 = MusicTrack(title="music1", user=self.user1)
        music1.save()
        collection.save()
        music1.collections.add(collection)

        collection2 = MusicCollection(title="name", user=self.user1)
        music2 = MusicTrack(title="music2", user=self.user1)
        music2.save()
        collection2.save()
        music2.collections.add(collection2)

        logged_in = self.client.login(
            username=self.user1.username, password="test_password"
        )

        response = self.client.get(
            reverse("music_collection:collection_detail", kwargs={"pk": collection.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, music1.title)
        self.assertNotContains(response, music2.title)

        response = self.client.get(
            reverse("music_collection:collection_detail", kwargs={"pk": collection2.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, music2.title)
        self.assertNotContains(response, music1.title)
