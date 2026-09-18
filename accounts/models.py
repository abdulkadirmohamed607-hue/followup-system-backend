from django.contrib.auth.models import AbstractUser
from django.db import models


class ModulePermission(models.Model):

    class Module(models.TextChoices):
        PATIENTS = 'PATIENTS', 'Patients'
        VISITOR_CHECK = 'VISITOR_CHECK', 'Visitor Check'
        REPORTS = 'REPORTS', 'Reports'
        USER_UPLOAD = 'USER_UPLOAD', 'User Upload'
        USER_MANAGEMENT = 'USER_MANAGEMENT', 'User Management'
        SYSTEM_SETTINGS = 'SYSTEM_SETTINGS', 'System Settings'

    module = models.CharField(
        max_length=30,
        choices=Module.choices,
        unique=True
    )

    name = models.CharField(
        max_length=100
    )

    description = models.CharField(
        max_length=255,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


class User(AbstractUser):

    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        USER = 'USER', 'User'

    phone = models.CharField(
        max_length=20,
        blank=True
    )

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.USER
    )

    must_change_password = models.BooleanField(
        default=True
    )

    module_permissions = models.ManyToManyField(
        ModulePermission,
        blank=True,
        related_name='users'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.username