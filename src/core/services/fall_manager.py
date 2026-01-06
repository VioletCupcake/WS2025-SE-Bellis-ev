"""
FallManager - Minimal business logic for atomic operations.
Most operations handled by Django ORM in views.
"""
from typing import Optional
from uuid import UUID
from django.db import transaction
from django.core.exceptions import ValidationError, PermissionDenied

from core.models import Fall, PersonenbezogeneDaten, User


class FallManager:
    """
    Service class for operations requiring atomic transactions or permission checks.
    Standard CRUD uses Django ORM directly in views.
    """
    
    @staticmethod
    @transaction.atomic
    def createFall(fall_data: dict, personen_data: dict) -> Fall:
        """
        Create Fall with PersonenbezogeneDaten atomically.
        
        Atomic transaction ensures both created together or not at all.
        This is the primary reason this service exists.
        
        Args:
            fall_data: Fall field values (zustaendige_beratungsstelle, etc.)
            personen_data: PersonenbezogeneDaten values (must include 'alias')
        
        Returns:
            Fall: Created case with linked PersonenbezogeneDaten
            
        Raises:
            ValidationError: If validation fails or alias already exists
        """
        # Check alias uniqueness
        alias = personen_data.get('alias')
        if not alias:
            raise ValidationError({'alias': ['Alias is required']})
        
        if PersonenbezogeneDaten.objects.filter(alias=alias).exists():
            raise ValidationError({'alias': [f'Alias "{alias}" already exists']})
        
        # Create Fall
        fall = Fall(**fall_data)
        fall.full_clean()
        fall.save()
        
        # Create linked PersonenbezogeneDaten
        personen = PersonenbezogeneDaten(fall=fall, **personen_data)
        personen.full_clean()
        personen.save()
        
        return fall
    
    @staticmethod
    def hardDeleteFall(fall_id: UUID, user: User) -> None:
        """
        Permanently delete Fall with permission check.
        
        Checks user permission before allowing deletion.
        CASCADE handles related data cleanup automatically.
        
        Args:
            fall_id: UUID of Fall to delete
            user: User attempting deletion
            
        Raises:
            PermissionDenied: If user lacks can_hard_delete_cases permission
            ValidationError: If user has no role assigned
            Fall.DoesNotExist: If fall_id not found
        """
        # Check user has role
        if not user.role:
            raise ValidationError(
                f"User {user.username} has no role assigned"
            )
        
        # Check permission
        if not user.role.permissions.can_hard_delete_cases:  # type: ignore[attr-defined]
            raise PermissionDenied(
                f"User {user.username} (role: {user.role.name}) lacks hard delete permission. "
                f"Required role: ADMINISTRATOR"
            )
        
        fall = Fall.objects.get(fall_id=fall_id)
        fall.delete()
