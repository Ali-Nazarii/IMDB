from rest_framework import filters, viewsets

from .models import Genre, Movie
from .serializers import GenreSerializer, MovieSerializer


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all().with_ratings().prefetch_related("genres")
    serializer_class = MovieSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "genres__name"]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
