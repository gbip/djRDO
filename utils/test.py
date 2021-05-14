from django.contrib.auth import get_user_model
from django.test import TestCase


class DjRDOTestHelper(TestCase):
    """
    Helper class that creates three user on test initialization : user, user1 and user2.
    """

    users = dict()

    @classmethod
    def _create_user(cls, username, password, email):
        user = get_user_model().objects.create(
            username=username, password=password, email=email
        )
        user.set_password(password)
        user.save()
        cls.users[username] = {"password": password, "email": email}
        setattr(cls, username, user)

    @classmethod
    def setUpTestData(cls):
        cls._create_user("user1", "test_password", "toto1@toto.com")
        cls._create_user("user2", "test_password", "toto2@toto.com")
        cls._create_user("user", "test_password", "toto@toto.com")

    def login(self, username):
        if (user_detail := self.users.get(username)) is not None:
            logged_in = self.client.login(
                username=username, password=user_detail["password"]
            )
            self.assertTrue(logged_in)
        else:
            raise Exception("{} failed to login", username)
