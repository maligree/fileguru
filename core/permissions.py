from rest_framework import exceptions, permissions


class HasProperPassphrase(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        auth_type, credentials = request.META["HTTP_AUTHORIZATION"].split(" ")
        if not obj.password == credentials:
            # WHy not just false? see issue TODO
            raise exceptions.PermissionDenied(
                "That's not the right passphrase. Keep guessing!"
            )
        else:
            return True
