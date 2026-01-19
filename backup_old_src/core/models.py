"""
Legacy models.py - redirects to modular structure.
"""
from django.db import models

from .models.user_models import *  # noqa

# This file kept for Django compatibility.
# All models defined in models/ package.
