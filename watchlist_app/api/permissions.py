from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admins to edit objects.
    All other users can only read.
    """

    def has_permission(self, request, view):
        # Check if the user is an admin
        if request.user and request.user.is_staff:
            return True
        # Allow read-only access for non-admin users
        return request.method in permissions.SAFE_METHODS

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the object.
        return obj.review_user == request.user