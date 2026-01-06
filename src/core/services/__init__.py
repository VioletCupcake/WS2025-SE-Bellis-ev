"""Business logic services for SE_B-EV_2025."""

from .validation_service import ValidationService, ValidationResult
from .fall_manager import FallManager

__all__ = ['ValidationService', 'ValidationResult', 'FallManager']