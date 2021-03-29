from django.contrib.auth import get_user_model

# Create your tests here.
from django.test import TestCase
from django.urls import reverse


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
