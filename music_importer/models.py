from django.db import models
from django.core.validators import MinValueValidator


# Create your models here.



class Artist(models.Model):
    name = models.CharField(max_length=5000)


class Album(models.Model):
    name = models.CharField(max_length=5000)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)


class Music(models.Model):
    title = models.CharField(max_length=5000)
    import_date = models.DateTimeField(auto_now_add=True)
    bpm = models.IntegerField(validators=[MinValueValidator(0, "Bpm must be positive")])
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    keu = models
    date_released = models.DateField
