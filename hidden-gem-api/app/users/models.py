from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Extended user model that adds a role field distinguishing between
    tourists (consumers of location data) and local guides (contributors).

    Inherits all standard Django auth fields: username, email, password,
    first_name, last_name, is_staff, is_active, date_joined, etc.
    """

    class Role(models.TextChoices):
        TOURIST = "tourist", "Tourist"
        LOCAL_GUIDE = "local_guide", "Local Guide"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.TOURIST,
        db_index=True,
        help_text="Designates whether this user is a tourist or a local guide.",
    )

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self) -> str:
        return f"{self.username} ({self.get_role_display()})"

    @property
    def is_local_guide(self) -> bool:
        """Convenience property to check if this user is a local guide."""
        return self.role == self.Role.LOCAL_GUIDE
