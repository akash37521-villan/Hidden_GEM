from django.contrib.gis.db import models as gis_models
from django.db import models
from django.conf import settings


class Location(models.Model):
    """
    Represents a hidden gem or local point of interest.

    Key design decisions:
    - `coordinates` uses PostGIS PointField with SRID=4326 (WGS84 / GPS standard).
      This enables all PostGIS spatial functions (ST_DWithin, ST_Distance, etc.)
      directly from Django ORM.
    - `created_by` FK to the custom user ensures only local guides can create
      locations (enforced at the view/permission level).
    - `db_index=True` on frequently filtered fields speeds up category/guide queries.
    """

    class Category(models.TextChoices):
        MOUNTAIN_TRAIL = "Mountain Trail", "Mountain Trail"
        COLONIAL_HERITAGE = "Colonial Heritage", "Colonial Heritage"
        MONASTERY = "Monastery", "Monastery"
        LOCAL_EATERY = "Local Eatery", "Local Eatery"
        SANCTUARY = "Sanctuary", "Sanctuary"
        VIEWPOINT = "Scenic Viewpoint", "Scenic Viewpoint"
        OTHER = "Other", "Other"

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.CharField(
        max_length=50,
        choices=Category.choices,
        default=Category.MOUNTAIN_TRAIL,
        db_index=True,
    )
    image_url = models.URLField(
        max_length=500,
        blank=True,
        help_text="High-resolution real photography URL from Unsplash.",
    )

    # --- Geospatial field ---
    # SRID 4326 = standard GPS coordinate system (lat/lng in WGS84 degrees).
    # geography=True stores data on a spheroid, making ST_DWithin use METRES.
    coordinates = gis_models.PointField(srid=4326, geography=True)

    # --- Relations ---
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="locations",
        db_index=True,
        help_text="The local guide who shared this gem.",
    )

    @property
    def created_by(self):
        """Backward compatibility alias."""
        return self.added_by

    # --- Timestamps ---
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Location"
        verbose_name_plural = "Locations"
        # Add a spatial index (GIST) on coordinates — essential for
        # fast ST_DWithin / ST_Distance queries over large datasets.
        indexes = [
            models.Index(fields=["category"]),
        ]

    def __str__(self) -> str:
        return f"{self.title} [{self.category}]"
