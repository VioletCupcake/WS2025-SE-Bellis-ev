"""
Views package for B-EV case management.

Exports all view modules for easy import in urls.py.
"""

from . import fall_views
from . import beratung_views
from . import gewalttat_views

__all__ = [
    'fall_views',
    'beratung_views',
    'gewalttat_views',
]

