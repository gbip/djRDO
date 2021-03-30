from django.contrib.auth import get_user_model

# Create your tests here.
from django.test import TestCase
from django.urls import reverse

from music_importer.models import MusicTrack


class TestAuthViewsBehaviour(TestCase):
    @classmethod
    def setUp(cls):
        cls.user = get_user_model().objects.create(
            username="test_user", password="test_password", email="nomail@nomail.com"
        )
        cls.user.set_password("test_password")
        cls.user.save()

    def test_navbar(self):
        response = self.client.get(reverse("accounts:login"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sign up")
        self.assertContains(response, "Log in")
        self.assertNotContains(response, "Import Music")
        self.assertNotContains(response, "Insights")

        self.assertTrue(
            self.client.login(username=self.user.username, password="test_password")
        )
        response = self.client.get(reverse("accounts:stats"))
        self.assertContains(response, self.user.username)
        self.assertNotContains(response, "Signup")
        self.assertNotContains(response, "Login")
        self.assertContains(response, "Import Music")
        self.assertContains(response, "Insights")

    def test_profile(self):
        self.assertTrue(
            self.client.login(username=self.user.username, password="test_password")
        )
        response = self.client.get(reverse("accounts:profile"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.email)
        for btn_text in ["Logout", "Change Password", "Delete Account"]:
            self.assertContains(response, btn_text)


class TestAccountMethod(TestCase):
    @classmethod
    def setUp(cls):
        cls.user = get_user_model().objects.create(
            username="test_user", password="test_password", email="nomail@nomail.com"
        )
        cls.user.set_password("test_password")
        cls.user.save()

    def test_user_track_deletion(self):
        resp = self.client.get(reverse("music_collection:delete_collection"))
        self.assertRedirects(
            resp, reverse("accounts:login") + "?next=%2Fmusic%2Fdelete_collection"
        )

        self.assertTrue(
            self.client.login(username=self.user.username, password="test_password")
        )
        track = MusicTrack(title="to be deleted", user=self.user)
        track.save()
        resp = self.client.post(reverse("music_collection:delete_collection"))
        self.assertEqual(resp.status_code, 200)
        user_tracks = MusicTrack.objects.filter(user=self.user)
        self.assertEqual(user_tracks.count(), 0)

        resp = self.client.post(reverse("music_collection:delete_collection"))
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get(reverse("music_collection:delete_collection"))
        self.assertEqual(resp.status_code, 405)

    def test_user_account_deletion(self):
        resp = self.client.get(reverse("accounts:delete_account"))
        self.assertRedirects(
            resp,
            reverse("accounts:login") + "?next=%2Faccounts%2Fdelete_account%2F",
        )

        self.assertTrue(
            self.client.login(username=self.user.username, password="test_password")
        )

        resp = self.client.get(reverse("accounts:delete_account"))
        self.assertEqual(resp.status_code, 405)

        resp = self.client.post(reverse("accounts:delete_account"))
        self.assertEqual(resp.status_code, 200)

        self.assertFalse(
            self.client.login(username=self.user.username, password="test_password")
        )
