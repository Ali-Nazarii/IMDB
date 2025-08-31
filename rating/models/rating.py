from typing import TYPE_CHECKING

from django.contrib.auth import get_user_model
from django.db import models

from movie.models import Movie

if TYPE_CHECKING:
    from user.models import User


class Rating(models.Model):
    user: "User" = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="ratings",
        related_query_name="rating",
    )
    movie: Movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name="ratings",
        related_query_name="rating",
    )
    score = models.PositiveSmallIntegerField(
        help_text="Rating score from 1 to 10",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "movie"], name="unique_user_movie_rating"
            ),
            models.CheckConstraint(
                check=models.Q(score__gte=1) & models.Q(score__lte=10),
                name="score_range_check",
            ),
        ]

    def __str__(self):
        return f"{self.user.username} → {self.movie.title}: {self.score}"
