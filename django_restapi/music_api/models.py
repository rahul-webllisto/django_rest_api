from django.db import models

# Create your models here.


class Song(models.Model):
    title = models.CharField(max_length=25)
    artist = models.CharField(max_length=25)

    def __str__(self):
        return "{} -by {}".format(self.title, self.artist)
