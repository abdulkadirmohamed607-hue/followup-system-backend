from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User
from .permissions import IsAdminRole
from .serializers import (
    AdminResetPasswordSerializer,
    ChangePasswordSerializer,
    LoginSerializer,
    UserCreateSerializer,
    UserListSerializer,
    UserUpdateSerializer,
)


# =========================================================
# LOGIN
# =========================================================

class LoginView(TokenObtainPairView):

    serializer_class = LoginSerializer


# =========================================================
# CHANGE OWN PASSWORD
# =========================================================

class ChangePasswordView(APIView):

    permission_classes = [IsAuthenticated]

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
                'message': 'Password changed successfully.',
                'must_change_password': False,
            },
            status=status.HTTP_200_OK
        )


# =========================================================
# CURRENT LOGGED-IN USER
# =========================================================

class CurrentUserView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        user = request.user

        return Response(
            {
                'id': user.id,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'phone': user.phone,
                'role': user.role,
                'must_change_password':
                    user.must_change_password,
                'is_active': user.is_active,
            },
            status=status.HTTP_200_OK
        )


# =========================================================
# USER MANAGEMENT
# ADMIN ONLY
# =========================================================

class UserViewSet(ModelViewSet):

    queryset = User.objects.all().order_by('-created_at')

    permission_classes = [IsAdminRole]

    # -----------------------------------------------------
    # SELECT SERIALIZER DEPENDING ON ACTION
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

        return UserListSerializer

    # -----------------------------------------------------
    # DELETE USER
    # -----------------------------------------------------

    def destroy(self, request, *args, **kwargs):

        user = self.get_object()

        # Prevent Admin from deleting their own account
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
    def reset_password(self, request, pk=None):

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