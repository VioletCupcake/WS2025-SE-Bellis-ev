"""
Custom permission decorators for B-EV case management.

Wraps PermissionSet boolean flags in Django-style decorators.
Used instead of Django's built-in @permission_required to support
custom business logic permissions (soft vs. hard delete, etc.).
"""

from functools import wraps
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required


def permission_required_custom(permission_flag):
    """
    Decorator that checks custom PermissionSet flags.
    
    Args:
        permission_flag (str): Name of boolean field in PermissionSet model
                              e.g., 'can_edit_cases', 'can_manage_reference_data'
    
    Usage:
        @login_required
        @permission_required_custom('can_edit_cases')
        def my_view(request):
            ...
    
    Raises:
        PermissionDenied: If user lacks required permission
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # Check user has role assigned
            if not hasattr(request.user, 'role') or request.user.role is None:
                raise PermissionDenied(
                    "Benutzer hat keine Rolle zugewiesen. Kontaktieren Sie einen Administrator."
                )
            
            # Check role has permissions configured
            if not hasattr(request.user.role, 'permissions'):
                raise PermissionDenied(
                    "Rolle hat keine Berechtigungen konfiguriert. Kontaktieren Sie einen Administrator."
                )
            
            # Check specific permission flag
            has_permission = getattr(request.user.role.permissions, permission_flag, False)
            
            if not has_permission:
                raise PermissionDenied(
                    f"Fehlende Berechtigung: {permission_flag}. "
                    f"Ihre Rolle ({request.user.role.name}) erlaubt diese Aktion nicht."
                )
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
