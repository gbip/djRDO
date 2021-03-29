from django.contrib.auth import get_user_model
from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.urls import reverse


class TestViewsAuthBehaviour(TestCase):
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
