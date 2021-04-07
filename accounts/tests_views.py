from django.contrib.auth import get_user_model

# Create your tests here.
from django.test import TestCase
from django.urls import reverse

from music_importer.models import MusicTrack
from utils.test import DjRDOTestHelper


class TestAuthViewsBehaviour(DjRDOTestHelper):
    """
    Test views behaviour related to authentication
    """

    def test_navbar(self):
        """
        Verify that the navbar does not dislay login based view to an anonymous user.
        :return:
        """
        response = self.client.get(reverse("accounts:login"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sign up")
        self.assertContains(response, "Log in")
        self.assertNotContains(response, "Import Music")
        self.assertNotContains(response, "Insights")
        self.assertNotContains(response, "Music Library")

        self.login("user")
        response = self.client.get(reverse("accounts:stats"))
        self.assertContains(response, self.user.username)
        self.assertNotContains(response, "Signup")
        self.assertNotContains(response, "Login")
        self.assertContains(response, "Import Music")
        self.assertContains(response, "Insights")
        self.assertContains(response, "Music Library")

    def test_profile(self):
        """
        Make sure that the profile page is login-only and display the required buttons.
        """
        self.assertRedirects(
            self.client.get(reverse("accounts:profile")),
            reverse("accounts:login") + "?next=" + reverse("accounts:profile"),
        )
        self.login("user")
        response = self.client.get(reverse("accounts:profile"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.email)
        for btn_text in [
            "Logout",
            "Change Password",
            "Delete Account",
            "Delete Music Collection",
        ]:
            self.assertContains(response, btn_text)


class TestAccountMethod(DjRDOTestHelper):
    """
    Test behaviour related to account POST method
    """

    def test_user_track_deletion(self):
        """
        Verify that track deletion works correctly
        """
        resp = self.client.get(reverse("music_collection:delete_collection"))
        self.assertRedirects(
            resp,
            reverse("accounts:login")
            + "?next="
            + reverse("music_collection:delete_collection"),
        )

        self.login("user")
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
        """
        Verify that account deletion behaves as expected
        """
        resp = self.client.get(reverse("accounts:delete_account"))
        self.assertRedirects(
            resp,
            reverse("accounts:login") + "?next=" + reverse("accounts:delete_account"),
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
