from django.contrib import admin
from django.db import models

from .models import Genre, Movie


class GenreAdmin(admin.ModelAdmin):
    list_display = ["name", "movie_count"]
    search_fields = ["name"]
    ordering = ["name"]

    def get_queryset(self, request):
        return (
            super().get_queryset(request).annotate(movie_count=models.Count("movies"))
        )

    def movie_count(self, obj):
        return obj.movie_count

    movie_count.short_description = "Number of Movies"
    movie_count.admin_order_field = "movie_count"


class MovieAdmin(admin.ModelAdmin):
    list_display = ["title", "creator", "created_by", "created_at", "genre_list"]
    list_filter = ["genres"]
    search_fields = ["title", "description", "creator", "created_by__username"]
    readonly_fields = ["uuid", "created_at", "updated_at"]
    filter_horizontal = ["genres"]
    raw_id_fields = ["created_by"]

    fieldsets = (
        ("Basic Information", {"fields": ("title", "description", "creator")}),
        ("Relationships", {"fields": ("genres", "created_by")}),
        (
            "System Information",
            {"fields": ("uuid", "created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("genres")

    def genre_list(self, obj):
        return ", ".join([genre.name for genre in obj.genres.all()])

    genre_list.short_description = "Genres"


admin.site.register(Movie, MovieAdmin)
admin.site.register(Genre, GenreAdmin)
