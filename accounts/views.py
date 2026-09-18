from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import ModulePermission, User
from .permissions import IsAdminRole
from .serializers import (
    AdminResetPasswordSerializer,
    ChangePasswordSerializer,
    CurrentUserSerializer,
    LoginSerializer,
    ModulePermissionSerializer,
    UserCreateSerializer,
    UserListSerializer,
    UserModulePermissionSerializer,
    UserUpdateSerializer,
)


# =========================================================
# LOGIN
# =========================================================

import time

class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):

        total_start = time.perf_counter()

        print('\n========================================')
        print('LOGIN DEBUG START')

        print('Before super().post():')
        step_start = time.perf_counter()

        response = super().post(
            request,
            *args,
            **kwargs
        )

        step_time = time.perf_counter() - step_start

        print(
            f'super().post() TIME: '
            f'{step_time:.6f} seconds'
        )

        total_time = (
            time.perf_counter()
            - total_start
        )

        print(
            f'FULL LoginView.post() TIME: '
            f'{total_time:.6f} seconds'
        )

        print('LOGIN DEBUG END')
        print('========================================\n')

        return response

# =========================================================
# CHANGE OWN PASSWORD
# =========================================================

class ChangePasswordView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def post(self, request):

        serializer = ChangePasswordSerializer(
            data=request.data,
            context={
                'request': request
            }
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return Response(
            {
                'message':
                    'Password changed successfully.',

                'must_change_password':
                    False,
            },
            status=status.HTTP_200_OK
        )


# =========================================================
# CURRENT LOGGED-IN USER
# =========================================================

class CurrentUserView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        serializer = CurrentUserSerializer(
            request.user
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


# =========================================================
# USER MANAGEMENT
# ADMIN ONLY
# =========================================================

class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all().order_by(
        '-created_at'
    )

    permission_classes = [
        IsAdminRole
    ]

    # -----------------------------------------------------
    # SELECT SERIALIZER
    # -----------------------------------------------------

    def get_serializer_class(self):

        if self.action == 'create':

            return UserCreateSerializer

        if self.action in [
            'update',
            'partial_update',
        ]:

            return UserUpdateSerializer

        if self.action == 'reset_password':

            return AdminResetPasswordSerializer

        if self.action == 'permissions':

            return UserModulePermissionSerializer

        return UserListSerializer

    # -----------------------------------------------------
    # DELETE USER
    # -----------------------------------------------------

    def destroy(
        self,
        request,
        *args,
        **kwargs
    ):

        user = self.get_object()

        # Prevent Admin from deleting
        # their own account.
        if user == request.user:

            return Response(
                {
                    'detail':
                        'You cannot delete your own account.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        user.delete()

        return Response(
            {
                'message':
                    'User deleted successfully.'
            },
            status=status.HTTP_200_OK
        )

    # -----------------------------------------------------
    # RESET USER PASSWORD
    # -----------------------------------------------------

    @action(
        detail=True,
        methods=['post'],
        url_path='reset-password'
    )
    def reset_password(
        self,
        request,
        pk=None
    ):

        user = self.get_object()

        serializer = AdminResetPasswordSerializer(
            data=request.data,
            context={
                'user': user
            }
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return Response(
            {
                'message':
                    'Password reset successfully.',

                'must_change_password':
                    True,
            },
            status=status.HTTP_200_OK
        )

    # -----------------------------------------------------
    # GET AVAILABLE MODULES
    # -----------------------------------------------------

    @action(
        detail=False,
        methods=['get'],
        url_path='modules'
    )
    def modules(self, request):

        modules = ModulePermission.objects.all()

        serializer = ModulePermissionSerializer(
            modules,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    # -----------------------------------------------------
    # GET / UPDATE USER PERMISSIONS
    # -----------------------------------------------------

    @action(
        detail=True,
        methods=['get', 'put'],
        url_path='permissions'
    )
    def permissions(
        self,
        request,
        pk=None
    ):

        user = self.get_object()

        # =================================================
        # GET USER PERMISSIONS
        # =================================================

        if request.method == 'GET':

            if user.role == User.Role.ADMIN:

                modules = list(
                    ModulePermission.objects.values_list(
                        'module',
                        flat=True
                    )
                )

            else:

                modules = list(
                    user.module_permissions.values_list(
                        'module',
                        flat=True
                    )
                )

            return Response(
                {
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'role': user.role,
                    },
                    'permissions': modules,
                },
                status=status.HTTP_200_OK
            )

        # =================================================
        # UPDATE USER PERMISSIONS
        # =================================================

        serializer = UserModulePermissionSerializer(
            data=request.data,
            context={
                'user': user
            }
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        # Return updated permissions.
        if user.role == User.Role.ADMIN:

            modules = list(
                ModulePermission.objects.values_list(
                    'module',
                    flat=True
                )
            )

        else:

            modules = list(
                user.module_permissions.values_list(
                    'module',
                    flat=True
                )
            )

        return Response(
            {
                'message':
                    'User permissions updated successfully.',

                'user': {
                    'id': user.id,
                    'username': user.username,
                    'role': user.role,
                },

                'permissions': modules,
            },
            status=status.HTTP_200_OK
        )