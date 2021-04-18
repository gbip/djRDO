from django.db import models

from djRDO import settings


class Artist(models.Model):
    """
    Artist model :
        * Name - String
        * User - Key to a User
    """

    name = models.CharField(max_length=5000)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
