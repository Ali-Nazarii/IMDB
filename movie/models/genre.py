from django.db import models


class GenreManager(models.Manager):
    pass


class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)

    objects: GenreManager = GenreManager()

    def __str__(self):
        return self.name
