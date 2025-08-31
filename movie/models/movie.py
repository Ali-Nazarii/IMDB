import uuid
from typing import TYPE_CHECKING

from django.contrib.auth import get_user_model
from django.db import models

from ..models import Genre

if TYPE_CHECKING:
    from user.models import User


class MovieManager(models.Manager):
    pass


class MovieQuerySet(models.QuerySet):
    def with_ratings(self):
        return self.annotate(
            avg_rating=models.Avg("rating__score"), rating_count=models.Count("rating")
        )


class Movie(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        null=False,
        blank=True,
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    genres = models.ManyToManyField(Genre, related_name="movies", blank=True)
    created_by: "User" = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="movies",
        related_query_name="movie",
    )
    creator = models.CharField(max_length=255, help_text="Creator of the movie")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects: MovieManager = MovieManager.from_queryset(MovieQuerySet)()

    def __str__(self):
        return self.title
