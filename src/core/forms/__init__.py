"""
Forms package for B-EV case management.

Exports all form classes for easy import in views.
"""

from .fall_forms import FallCreateForm
from .beratung_forms import BeratungForm
from .gewalttat_forms import GewalttatForm, TAETER_GESCHLECHT_CHOICES, TAETER_VERHAELTNIS_CHOICES
from .folgen_forms import FolgenDerGewaltForm
from .anfrage_forms import AnfrageCreateForm, AnfrageEditForm

__all__ = [
    'FallCreateForm',
    'BeratungForm',
    'GewalttatForm',
    'FolgenDerGewaltForm',
    'AnfrageCreateForm',
    'AnfrageEditForm',
    'TAETER_GESCHLECHT_CHOICES',
    'TAETER_VERHAELTNIS_CHOICES',
]
