from rest_framework import permissions


class IsHistoricOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.org == request.user.profile.org:
            return True
        return False