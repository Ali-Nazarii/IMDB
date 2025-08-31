from django.db import transaction
from rest_framework import serializers

from .models import Genre, Movie


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["id", "name"]


class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    genre_ids = serializers.PrimaryKeyRelatedField(
        queryset=Genre.objects.all(), many=True, write_only=True, source="genres"
    )

    class Meta:
        model = Movie
        fields = [
            "uuid",
            "title",
            "description",
            "genres",
            "genre_ids",
            "creator",
            "created_at",
            "updated_at",
        ]

    def validate_genre_ids(self, value):
        if not value:
            return value

        genre_ids = [genre.id for genre in value]
        existing_genres = Genre.objects.filter(id__in=genre_ids)

        if len(existing_genres) != len(genre_ids):
            existing_ids = set(existing_genres.values_list("id", flat=True))
            invalid_ids = set(genre_ids) - existing_ids
            raise serializers.ValidationError(f"Invalid genre IDs: {list(invalid_ids)}")

        return value

    @transaction.atomic
    def create(self, validated_data):
        genres = validated_data.pop("genres", [])
        movie = Movie.objects.create(**validated_data)
        if genres:
            movie.genres.set(genres)
        return movie

    def update(self, instance, validated_data):
        genres = validated_data.pop("genres", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if genres is not None:
            instance.genres.set(genres)

        instance.save()
        return instance
