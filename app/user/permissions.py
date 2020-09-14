from rest_framework.permissions import BasePermission, SAFE_METHODS


class EditUserPermission(BasePermission):
    """Limit user to edit only his profile."""

    def has_object_permission(self, request, view, obj):
        """Determine user permission."""
        if request.method in SAFE_METHODS:
            return True

        return bool(request.user.id == obj.id)
