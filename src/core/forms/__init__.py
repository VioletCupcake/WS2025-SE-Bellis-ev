"""
Forms package for B-EV case management.

Exports all form classes for easy import in views.
"""

from .fall_forms import FallCreateForm
from .beratung_forms import BeratungForm
from .gewalttat_forms import GewalttatForm

__all__ = [
    'FallCreateForm',
    'BeratungForm',
    'GewalttatForm',
]
