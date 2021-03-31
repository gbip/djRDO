from django.contrib.auth import get_user_model
from django.test import TestCase


class TestMusicCollection(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create(
            username="user", password="test_password", email="toto@toto.com"
        )
        cls.user.set_password("test_password")
        cls.user.save()
