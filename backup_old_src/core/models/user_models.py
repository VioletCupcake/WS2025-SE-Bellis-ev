"""
User authentication and permission models.
Implements 3-tier role system: BASIS, ERWEITERT, ADMINISTRATOR.
Also has Sessions and permissions
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
    Custom permission flags for role-based access control.
    
    Each Role has exactly one PermissionSet (1:1 relationship).
    Boolean flags define granular permissions beyond Django's default CRUD.
    
    Permission Matrix (as configured in seed_data.json):
    
    BASIS Role:
        - can_view_cases: True (read access to all cases)
        - can_edit_cases: True (create/update cases, add Beratung/Gewalttat)
        - can_delete_cases: False
        - can_hard_delete_cases: False
        - can_manage_reference_data: False
        - can_manage_users: False
        - can_assign_roles: False
    
    ERWEITERT Role:
        - can_view_cases: True
        - can_edit_cases: True
        - can_delete_cases: True (soft delete - archive cases)
        - can_hard_delete_cases: False
        - can_manage_reference_data: True (add/edit GewalttatArt, FolgenDerGewalt)
        - can_manage_users: False
        - can_assign_roles: False
    
    ADMINISTRATOR Role:
        - can_view_cases: True
        - can_edit_cases: True
        - can_delete_cases: True
        - can_hard_delete_cases: True (permanent deletion with CASCADE)
        - can_manage_reference_data: True
        - can_manage_users: True (create/edit/delete User records)
        - can_assign_roles: True (change User.role)
    
    Usage in views:
        Use @permission_required_custom decorator from core.decorators
        
        Example:
            @login_required
            @permission_required_custom('can_edit_cases')
            def case_create(request):
                ...
    
    Business Logic Notes:
        - can_delete_cases: Soft delete only (sets status='ARCHIVIERT')
        - can_hard_delete_cases: Permanent deletion (CASCADE to related entities)
        - can_manage_reference_data: ERWEITERT role's primary differentiator
    """
    
    permission_set_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    
    role = models.OneToOneField(
        'Role',
        on_delete=models.CASCADE,
        related_name='permissions'
    )
    
    # Case management permissions
    can_view_cases = models.BooleanField(
        default=False,  # ← FIXED: Changed from True to False (security-first)
        help_text="Erlaubt das Anzeigen von Fällen"
    )
    
    can_edit_cases = models.BooleanField(
        default=False,
        help_text="Erlaubt das Erstellen und Bearbeiten von Fällen, Beratungen und Gewalttaten"
    )
    
    can_delete_cases = models.BooleanField(
        default=False,
        help_text="Erlaubt das Archivieren von Fällen (Soft Delete)"
    )
    
    can_hard_delete_cases = models.BooleanField(
        default=False,
        help_text="Erlaubt das permanente Löschen von Fällen (Hard Delete mit CASCADE)"
    )
    
    # Reference data permissions
    can_manage_reference_data = models.BooleanField(
        default=False,
        help_text="Erlaubt das Hinzufügen und Bearbeiten von GewalttatArt und FolgenDerGewalt"
    )
    
    # User management permissions
    can_manage_users = models.BooleanField(
        default=False,
        help_text="Erlaubt das Erstellen, Bearbeiten und Löschen von Benutzern"
    )
    
    can_assign_roles = models.BooleanField(
        default=False,
        help_text="Erlaubt das Zuweisen und Ändern von Benutzerrollen"
    )
    
    def __str__(self):
        return f"Permissions for {self.role.name}"
    
    class Meta:
        db_table = 'permission_set'
        verbose_name = "Permission Set"
        verbose_name_plural = "Permission Sets"



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
