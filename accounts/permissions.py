from rest_framework.permissions import BasePermission


class IsAdminRole(BasePermission):
    """
    Allows access only to authenticated users
    whose FollowUp System role is ADMIN.
    """

    message = (
        'Only administrators are allowed '
        'to perform this action.'
    )

    def has_permission(self, request, view):

        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == 'ADMIN'
        )


class HasModulePermission(BasePermission):
    """
    Allows authenticated users to access a module.

    Administrators automatically have access
    to every module.

    Normal users must have the requested module
    assigned to them.
    """

    message = (
        'You do not have permission '
        'to access this module.'
    )

    def has_permission(self, request, view):

        user = request.user

        if not user or not user.is_authenticated:
            return False

        # Admin has access to every module.
        if user.role == 'ADMIN':
            return True

        module = getattr(
            view,
            'required_module',
            None
        )

        if not module:
            return False

        return user.module_permissions.filter(
            module=module
        ).exists()