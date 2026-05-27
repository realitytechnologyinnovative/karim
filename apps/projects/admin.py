from django.contrib import admin

from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "location", "year", "is_published", "updated_at")
    list_filter = ("is_published", "year")
    search_fields = ("title", "description", "location")
    prepopulated_fields = {"slug": ("title",)}
