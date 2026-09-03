from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User


class LoginSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['user_id'] = user.id
        token['username'] = user.username
        token['role'] = user.role
        token['must_change_password'] = user.must_change_password

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        user = self.user

        data['user'] = {
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'phone': user.phone,
            'role': user.role,
            'must_change_password': user.must_change_password,
            'is_active': user.is_active,
        }

        return data


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

        new_password = attrs.get('new_password')
        confirm_password = attrs.get('confirm_password')

        if new_password != confirm_password:
            raise serializers.ValidationError({
                'confirm_password':
                    'New password and confirmation password do not match.'
            })

        if attrs.get('old_password') == new_password:
            raise serializers.ValidationError({
                'new_password':
                    'New password must be different from the current password.'
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


class UserListSerializer(serializers.ModelSerializer):

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
        ]

        read_only_fields = [
            'id',
            'date_joined',
            'created_at',
            'updated_at',
        ]


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

        password = validated_data.pop('password')

        user = User(
            **validated_data
        )

        user.set_password(password)

        user.must_change_password = True

        user.save()

        return user


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


class AdminResetPasswordSerializer(serializers.Serializer):

    new_password = serializers.CharField(
        write_only=True,
        validators=[validate_password]
    )

    confirm_password = serializers.CharField(
        write_only=True
    )

    def validate(self, attrs):

        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({
                'confirm_password':
                    'New password and confirmation password do not match.'
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