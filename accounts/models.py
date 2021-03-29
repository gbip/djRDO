from django.contrib.auth.models import AbstractUser

# Create your models here.
from django.db.models import EmailField


class DjRdoUser(AbstractUser):
    """
    Extends the django user with a required email field
    """

    email = EmailField("email address", blank=False, null=False)
