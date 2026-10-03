from django.contrib import admin
from django.contrib.gis import admin as gis_admin
from .models import Location


@admin.register(Location)
class LocationAdmin(gis_admin.GISModelAdmin):
    """Admin for Location with an interactive map widget for the PointField."""
    list_display = ("title", "category", "created_by", "created_at")
    list_filter = ("category",)
    search_fields = ("title", "description")
    readonly_fields = ("created_at", "updated_at")
