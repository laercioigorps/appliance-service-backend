from rest_framework.permissions import BasePermission


class IsServiceOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.profile.org == obj.owner:
            return True
        return False
