from rest_framework.permissions import BasePermission


class IsAdminRole(BasePermission):
    """
    Allows access only to authenticated users
    whose FollowUp System role is ADMIN.
    """

    message = 'Only administrators are allowed to perform this action.'

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == 'ADMIN'
        )