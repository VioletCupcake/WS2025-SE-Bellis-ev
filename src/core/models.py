from django.db import models

# Create your models here.
"""
Legacy models.py - redirects to modular structure.
"""
from .models.user_models import *  # noqa

# This file kept for Django compatibility.
# All models defined in models/ package.
