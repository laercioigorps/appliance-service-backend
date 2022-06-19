from rest_framework import permissions


class IsCustomerOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user.profile.org:
            return True
        return False
