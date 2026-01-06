"""Validation service for core business logic.
Format and type validation before database commit.
"""
from datetime import date, datetime
from typing import Any, List, Optional
from uuid import UUID
import re


class ValidationResult:
    """Stores validation results with error aggregation."""
    
    def __init__(self):
        self.is_valid: bool = True
        self.errors: List[str] = []
    
    def add_error(self, error: str) -> None:
        """Add validation error and mark result as invalid."""
        self.is_valid = False
        self.errors.append(error)
    
    def get_summary(self) -> str:
        """Return formatted error summary."""
        if self.is_valid:
            return "Validation passed"
        return f"Validation failed: {'; '.join(self.errors)}"
    
    def __bool__(self) -> bool:
        """Allow truthiness check: if result: ..."""
        return self.is_valid


class ValidationService:
    """
    Stateless validation service for format/type checking.
    Does NOT perform business logic validation (use model.clean() for that).
    """
    
    @staticmethod
    def validate_date(date_string: str) -> bool:
        """
        Validate date string in ISO format (YYYY-MM-DD).
        
        Args:
            date_string: String representation of date
            
        Returns:
            True if valid date format, False otherwise
        """
        if not date_string:
            return False
        try:
            datetime.strptime(date_string, "%Y-%m-%d")
            return True
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def validate_number(number_string: str, allow_float: bool = False) -> bool:
        """
        Validate numeric string.
        
        Args:
            number_string: String representation of number
            allow_float: If True, accept decimal numbers
            
        Returns:
            True if valid number format, False otherwise
        """
        if not number_string:
            return False
        try:
            if allow_float:
                float(number_string)
            else:
                int(number_string)
            return True
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def validate_enum(value: Any, allowed_values: List[str]) -> bool:
        """
        Validate value against allowed enum choices.
        
        Args:
            value: Value to check
            allowed_values: List of permitted values
            
        Returns:
            True if value in allowed list, False otherwise
        """
        return value in allowed_values
    
    @staticmethod
    def validate_integer_range(value: int, min_val: Optional[int] = None, 
                               max_val: Optional[int] = None) -> bool:
        """
        Validate integer within range.
        
        Args:
            value: Integer to validate
            min_val: Minimum allowed value (inclusive)
            max_val: Maximum allowed value (inclusive)
            
        Returns:
            True if within range, False otherwise
        """
        if not isinstance(value, int):
            return False
        if min_val is not None and value < min_val:
            return False
        if max_val is not None and value > max_val:
            return False
        return True
    
    @staticmethod
    def validate_float_range(value: float, min_val: Optional[float] = None,
                            max_val: Optional[float] = None) -> bool:
        """
        Validate float within range.
        
        Args:
            value: Float to validate
            min_val: Minimum allowed value (inclusive)
            max_val: Maximum allowed value (inclusive)
            
        Returns:
            True if within range, False otherwise
        """
        if not isinstance(value, (int, float)):
            return False
        if min_val is not None and value < min_val:
            return False
        if max_val is not None and value > max_val:
            return False
        return True
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """
        Basic email format validation.
        Django's EmailField handles this, but useful for pre-validation.
        
        Args:
            email: Email address string
            
        Returns:
            True if valid email format, False otherwise
        """
        if not email:
            return False
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_uuid(uuid_string: str) -> bool:
        """
        Validate UUID format.
        
        Args:
            uuid_string: String representation of UUID
            
        Returns:
            True if valid UUID format, False otherwise
        """
        try:
            UUID(uuid_string)
            return True
        except (ValueError, TypeError, AttributeError):
            return False
    
    @staticmethod
    def validate_string_length(value: str, max_length: int, 
                               min_length: int = 0) -> bool:
        """
        Validate string length constraints.
        
        Args:
            value: String to validate
            max_length: Maximum allowed length
            min_length: Minimum required length
            
        Returns:
            True if length within bounds, False otherwise
        """
        if not isinstance(value, str):
            return False
        length = len(value)
        return min_length <= length <= max_length
    
    @classmethod
    def validate_input(cls, input_data: dict, field_name: str, 
                      field_type: str, **kwargs) -> ValidationResult:
        """
        Generic input validation dispatcher.
        
        Args:
            input_data: Dictionary containing field data
            field_name: Name of field to validate
            field_type: Type identifier (date, integer, float, email, etc.)
            **kwargs: Additional validation parameters (min, max, choices, etc.)
            
        Returns:
            ValidationResult object
        """
        result = ValidationResult()
        value = input_data.get(field_name)
        
        # Handle null/empty values
        if value is None or value == '':
            if kwargs.get('required', False):
                result.add_error(f"{field_name} is required")
            return result
        
        # Type-specific validation
        if field_type == 'date':
            if not cls.validate_date(str(value)):
                result.add_error(f"{field_name} must be valid date (YYYY-MM-DD)")
        
        elif field_type == 'integer':
            if not cls.validate_number(str(value), allow_float=False):
                result.add_error(f"{field_name} must be an integer")
            elif kwargs.get('min') is not None or kwargs.get('max') is not None:
                if not cls.validate_integer_range(int(value), 
                                                 kwargs.get('min'), 
                                                 kwargs.get('max')):
                    result.add_error(f"{field_name} out of range")
        
        elif field_type == 'float':
            if not cls.validate_number(str(value), allow_float=True):
                result.add_error(f"{field_name} must be a number")
            elif kwargs.get('min') is not None or kwargs.get('max') is not None:
                if not cls.validate_float_range(float(value),
                                               kwargs.get('min'),
                                               kwargs.get('max')):
                    result.add_error(f"{field_name} out of range")
        
        elif field_type == 'email':
            if not cls.validate_email(str(value)):
                result.add_error(f"{field_name} must be valid email")
        
        elif field_type == 'enum':
            choices = kwargs.get('choices', [])
            if not cls.validate_enum(value, choices):
                result.add_error(f"{field_name} must be one of {choices}")
        
        elif field_type == 'string':
            max_len = kwargs.get('max_length', 999999)
            min_len = kwargs.get('min_length', 0)
            if not cls.validate_string_length(str(value), max_len, min_len):
                result.add_error(f"{field_name} length must be {min_len}-{max_len}")
        
        return result
