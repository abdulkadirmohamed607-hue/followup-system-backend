from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from accounts.permissions import HasModulePermission
from .models import SessionSetting
from .serializers import SessionSettingSerializer


class CanReadSessionSettings(IsAuthenticated):
    """
    Allows authenticated users who have either:

    - VISITOR_CHECK
    - SYSTEM_SETTINGS

    permission.

    This permission is only used for READ operations.
    """

    message = (
        'You do not have permission '
        'to access session settings.'
    )

    def has_permission(self, request, view):

        user = request.user

        if not user or not user.is_authenticated:
            return False

        # Admin can always read session settings.
        if user.role == 'ADMIN':
            return True

        return (
            user.module_permissions.filter(
                module='VISITOR_CHECK'
            ).exists()
            or
            user.module_permissions.filter(
                module='SYSTEM_SETTINGS'
            ).exists()
        )


class SessionSettingViewSet(ViewSet):

    permission_classes = [
        IsAuthenticated,
        HasModulePermission,
    ]

    required_module = 'SYSTEM_SETTINGS'

    def get_permissions(self):

        # -------------------------------------------------
        # READ OPERATIONS
        # -------------------------------------------------
        # Visitor Check users need to READ the session
        # configuration so the system can determine
        # Morning / Day / Evening.
        #
        # They are NOT being given permission to modify
        # System Settings.
        # -------------------------------------------------

        if self.action in [
            'list',
            'retrieve'
        ]:

            return [
                CanReadSessionSettings()
            ]

        # -------------------------------------------------
        # WRITE OPERATIONS
        # -------------------------------------------------
        # Only users with SYSTEM_SETTINGS permission
        # can modify session settings.
        # -------------------------------------------------

        return [
            IsAuthenticated(),
            HasModulePermission()
        ]

    def list(self, request):

        settings = SessionSetting.objects.all()

        serializer = SessionSettingSerializer(
            settings,
            many=True
        )

        return Response(
            serializer.data
        )

    def retrieve(
        self,
        request,
        pk=None
    ):

        try:

            session_setting = (
                SessionSetting.objects.get(
                    pk=pk
                )
            )

        except SessionSetting.DoesNotExist:

            return Response(
                {
                    'detail':
                    'Session setting not found.'
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = SessionSettingSerializer(
            session_setting
        )

        return Response(
            serializer.data
        )

    def update(
        self,
        request,
        pk=None
    ):

        try:

            session_setting = (
                SessionSetting.objects.get(
                    pk=pk
                )
            )

        except SessionSetting.DoesNotExist:

            return Response(
                {
                    'detail':
                    'Session setting not found.'
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = SessionSettingSerializer(
            session_setting,
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return Response(
            serializer.data
        )

    def partial_update(
        self,
        request,
        pk=None
    ):

        try:

            session_setting = (
                SessionSetting.objects.get(
                    pk=pk
                )
            )

        except SessionSetting.DoesNotExist:

            return Response(
                {
                    'detail':
                    'Session setting not found.'
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = SessionSettingSerializer(
            session_setting,
            data=request.data,
            partial=True
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return Response(
            serializer.data
        )