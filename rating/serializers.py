from rest_framework import serializers

from movie.models import Movie

from .models import Rating


class RatingSerializer(serializers.ModelSerializer):
    movie_uuid = serializers.UUIDField(write_only=True)
    movie_title = serializers.CharField(source="movie.title", read_only=True)
    user_username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Rating
        fields = [
            "id",
            "movie_uuid",
            "movie_title",
            "user_username",
            "score",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "user_username"]

    def validate_score(self, value):
        if not 1 <= value <= 10:
            raise serializers.ValidationError("Score must be between 1 and 10")
        return value

    def validate_movie_uuid(self, value):
        """Validate that the movie exists"""
        try:
            Movie.objects.get(uuid=value)
        except Movie.DoesNotExist:
            raise serializers.ValidationError("Movie not found")
        return value

    def create(self, validated_data):
        movie_uuid = validated_data.pop("movie_uuid")
        movie = Movie.objects.get(uuid=movie_uuid)

        validated_data["movie"] = movie

        user = self.context["request"].user
        if Rating.objects.filter(user=user, movie=movie).exists():
            raise serializers.ValidationError("You have already rated this movie")

        return super().create(validated_data)

    def update(self, instance, validated_data):
        if "movie_uuid" in validated_data:
            movie_uuid = validated_data.pop("movie_uuid")
            try:
                movie = Movie.objects.get(uuid=movie_uuid)
                validated_data["movie"] = movie
            except Movie.DoesNotExist:
                raise serializers.ValidationError("Movie not found")

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
