from django.contrib import admin

from .models import Rating


class RatingAdmin(admin.ModelAdmin):
    list_display = ["user", "movie", "score", "created_at", "updated_at"]
    list_filter = ["score", "created_at", "updated_at"]
    search_fields = ["user__username", "movie__title", "score"]
    readonly_fields = ["created_at", "updated_at"]
    autocomplete_fields = ["user", "movie"]
    ordering = ["-created_at"]

    fieldsets = (
        ("Rating Information", {"fields": ("user", "movie", "score")}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    def user_username(self, obj):
        """Display username for better readability"""
        return obj.user.username

    user_username.short_description = "Username"
    user_username.admin_order_field = "user__username"

    def movie_title(self, obj):
        """Display movie title for better readability"""
        return obj.movie.title

    movie_title.short_description = "Movie Title"
    movie_title.admin_order_field = "movie__title"


admin.site.register(Rating, RatingAdmin)
