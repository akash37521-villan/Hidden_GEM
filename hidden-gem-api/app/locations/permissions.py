from rest_framework import permissions


class IsLocalGuideOrReadOnly(permissions.BasePermission):
    """
    Custom permission:
    - Safe methods (GET, HEAD, OPTIONS) → allowed for everyone, including
      unauthenticated users.
    - Write methods (POST, PUT, PATCH, DELETE) → only allowed for
      authenticated users whose role is 'local_guide'.

    This prevents tourists from submitting locations while still exposing
    the read API publicly.
    """

    def has_permission(self, request, view) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            request.user
            and request.user.is_authenticated
            and request.user.is_local_guide
        )

    def has_object_permission(self, request, view, obj) -> bool:
        """For object-level writes, the user must also be the creator/guide who added it."""
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.added_by == request.user
