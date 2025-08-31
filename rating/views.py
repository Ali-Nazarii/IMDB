from rest_framework import permissions, viewsets

from .models import Rating
from .serializers import RatingSerializer


class RatingViewSet(viewsets.ModelViewSet):
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Return only ratings for the current user"""
        return Rating.objects.filter(user=self.request.user).select_related(
            "movie", "user"
        )

    def perform_create(self, serializer):
        """Set the user and handle create/update logic"""
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        """Ensure user can only update their own ratings"""
        serializer.save(user=self.request.user)
