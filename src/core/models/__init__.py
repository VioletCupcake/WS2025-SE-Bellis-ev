
"""
Core models package
Imports all models for Django to discover.
"""
from .user_models import User, Role, PermissionSet, Session
from .fall_models import Fall, PersonenbezogeneDaten, Beratung, Gewalttat

__all__ = [
    'User', 'Role', 'PermissionSet', 'Session',
    'Fall', 'PersonenbezogeneDaten', 'Beratung', 'Gewalttat'
]