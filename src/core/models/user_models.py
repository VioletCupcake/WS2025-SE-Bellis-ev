"""
User authentication and permission models.
Implements 3-tier role system: BASIS, ERWEITERT, ADMINISTRATOR.
"""
import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.Model):
    """
    Role definition with 3 fixed types.
    """
    ROLE_CHOICES = [
        ('BASIS', 'Basis'),
        ('ERWEITERT', 'Erweitert'),
        ('ADMIN', 'Administrator'),
    ]
    
    role_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20, choices=ROLE_CHOICES, unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        db_table = 'role'
        verbose_name = 'Rolle'
        verbose_name_plural = 'Rollen'
    
    def __str__(self):
        return self.get_name_display() # pyright: ignore[reportAttributeAccessIssue]


class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    Links to Role for permission management.
    """
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.ForeignKey(
        Role,
        on_delete=models.RESTRICT,
        related_name='users',
        null=True,  # Allow null temporarily for migration
        blank=True
    )
    
    class Meta:
        db_table = 'user'
        verbose_name = 'Benutzer'
        verbose_name_plural = 'Benutzer'
    
    def __str__(self):
        return self.username


class PermissionSet(models.Model):
    """
    Permission flags linked 1:1 to Role.
    """
    permission_set_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.OneToOneField(
        Role,
        on_delete=models.CASCADE,
        related_name='permissions'
    )
    can_view_cases = models.BooleanField(default=True)
    can_edit_cases = models.BooleanField(default=False)
    can_delete_cases = models.BooleanField(default=False)
    can_manage_reference_data = models.BooleanField(default=False)
    can_manage_users = models.BooleanField(default=False)
    can_assign_roles = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'permission_set'
        verbose_name = 'Berechtigungssatz'
        verbose_name_plural = 'Berechtigungssätze'
    
    def __str__(self):
        return f"Permissions for {self.role.name}"


class Session(models.Model):
    """
    User session tracking.
    """
    session_id = models.CharField(primary_key=True, max_length=40)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sessions'
    )
    start_time = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'session'
        verbose_name = 'Sitzung'
        verbose_name_plural = 'Sitzungen'
    
    def __str__(self):
        return f"Session for {self.user.username}"
