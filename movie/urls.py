from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import GenreViewSet, MovieViewSet

router = DefaultRouter()
router.register(r"movies", MovieViewSet, basename="movie")
router.register(r"genres", GenreViewSet, basename="genre")

urlpatterns = [
    path("", include(router.urls)),
]
