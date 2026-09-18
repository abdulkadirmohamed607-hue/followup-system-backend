from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import ModulePermission, User


# =========================================================
# LOGIN
# =========================================================

class LoginSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):

        token = super().get_token(user)

        token['user_id'] = user.id
        token['username'] = user.username
        token['role'] = user.role
        token['must_change_password'] = (
            user.must_change_password
        )

        return token

    def validate(self, attrs):

        # Django / SimpleJWT performs authentication here.
        data = super().validate(attrs)

        user = self.user

        # =================================================
        # USER MODULE PERMISSIONS
        # =================================================

        # Admin automatically has access to every module.
        if user.role == User.Role.ADMIN:

            permissions = list(
                ModulePermission.objects.values_list(
                    'module',
                    flat=True
                )
            )

        else:

            permissions = list(
                user.module_permissions.values_list(
                    'module',
                    flat=True
                )
            )

        # =================================================
        # LOGIN USER RESPONSE
        # =================================================

        data['user'] = {
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'phone': user.phone,
            'role': user.role,
            'must_change_password': (
                user.must_change_password
            ),
            'is_active': user.is_active,
            'permissions': permissions,
        }

        return data


# =========================================================
# CHANGE PASSWORD
# =========================================================

class ChangePasswordSerializer(serializers.Serializer):

    old_password = serializers.CharField(
        write_only=True
    )

    new_password = serializers.CharField(
        write_only=True,
        validators=[validate_password]
    )

    confirm_password = serializers.CharField(
        write_only=True
    )

    def validate_old_password(self, value):

        user = self.context['request'].user

        if not user.check_password(value):

            raise serializers.ValidationError(
                'Current password is incorrect.'
            )

        return value

    def validate(self, attrs):

        new_password = attrs.get(
            'new_password'
        )

        confirm_password = attrs.get(
            'confirm_password'
        )

        if new_password != confirm_password:

            raise serializers.ValidationError({
                'confirm_password':
                    'New password and confirmation '
                    'password do not match.'
            })

        if (
            attrs.get('old_password')
            == new_password
        ):

            raise serializers.ValidationError({
                'new_password':
                    'New password must be different '
                    'from the current password.'
            })

        return attrs

    def save(self, **kwargs):

        user = self.context['request'].user

        user.set_password(
            self.validated_data['new_password']
        )

        user.must_change_password = False

        user.save(
            update_fields=[
                'password',
                'must_change_password',
                'updated_at',
            ]
        )

        return user


# =========================================================
# CURRENT USER
# =========================================================

class CurrentUserSerializer(serializers.ModelSerializer):

    permissions = serializers.SerializerMethodField()

    class Meta:
        model = User

        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'phone',
            'role',
            'must_change_password',
            'is_active',
            'permissions',
        ]

    def get_permissions(self, obj):

        # Admin automatically has every module.
        if obj.role == User.Role.ADMIN:

            return [
                module.module
                for module in ModulePermission.objects.all()
            ]

        return list(
            obj.module_permissions.values_list(
                'module',
                flat=True
            )
        )


# =========================================================
# USER LIST
# =========================================================

class UserListSerializer(serializers.ModelSerializer):

    permissions = serializers.SerializerMethodField()

    class Meta:
        model = User

        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'phone',
            'role',
            'must_change_password',
            'is_active',
            'date_joined',
            'created_at',
            'updated_at',
            'permissions',
        ]

        read_only_fields = [
            'id',
            'date_joined',
            'created_at',
            'updated_at',
            'permissions',
        ]

    def get_permissions(self, obj):

        # Admin automatically has all modules.
        if obj.role == User.Role.ADMIN:

            return [
                module.module
                for module in ModulePermission.objects.all()
            ]

        return list(
            obj.module_permissions.values_list(
                'module',
                flat=True
            )
        )


# =========================================================
# CREATE USER
# =========================================================

class UserCreateSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        validators=[validate_password]
    )

    class Meta:
        model = User

        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'phone',
            'role',
            'password',
        ]

    def create(self, validated_data):

        password = validated_data.pop(
            'password'
        )

        user = User(
            **validated_data
        )

        user.set_password(password)

        user.must_change_password = True

        user.save()

        return user


# =========================================================
# UPDATE USER
# =========================================================

class UserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User

        fields = [
            'first_name',
            'last_name',
            'email',
            'phone',
            'role',
            'is_active',
        ]

        read_only_fields = [
            'username',
        ]


# =========================================================
# ADMIN RESET PASSWORD
# =========================================================

class AdminResetPasswordSerializer(serializers.Serializer):

    new_password = serializers.CharField(
        write_only=True,
        validators=[validate_password]
    )

    confirm_password = serializers.CharField(
        write_only=True
    )

    def validate(self, attrs):

        if (
            attrs['new_password']
            != attrs['confirm_password']
        ):

            raise serializers.ValidationError({
                'confirm_password':
                    'New password and confirmation '
                    'password do not match.'
            })

        return attrs

    def save(self, **kwargs):

        user = self.context['user']

        user.set_password(
            self.validated_data['new_password']
        )

        user.must_change_password = True

        user.save(
            update_fields=[
                'password',
                'must_change_password',
                'updated_at',
            ]
        )

        return user


# =========================================================
# MODULE PERMISSION LIST
# =========================================================

class ModulePermissionSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = ModulePermission

        fields = [
            'id',
            'module',
            'name',
            'description',
        ]

        read_only_fields = [
            'id',
            'module',
            'name',
            'description',
        ]


# =========================================================
# ASSIGN USER MODULE PERMISSIONS
# =========================================================

class UserModulePermissionSerializer(
    serializers.Serializer
):

    modules = serializers.ListField(
        child=serializers.ChoiceField(
            choices=ModulePermission.Module.choices
        ),
        allow_empty=True
    )

    def validate_modules(self, value):

        # Remove duplicate module names while
        # preserving their original order.
        return list(
            dict.fromkeys(value)
        )

    def save(self, **kwargs):

        user = self.context['user']

        # Admin permissions are automatic.
        if user.role == User.Role.ADMIN:

            return user

        module_permissions = (
            ModulePermission.objects.filter(
                module__in=self.validated_data[
                    'modules'
                ]
            )
        )

        user.module_permissions.set(
            module_permissions
        )

        return user