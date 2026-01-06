"""
Custom validators for JSONField structures.
Enforces schema for Gewalttat.taeterinnen_details.
"""
from django.core.exceptions import ValidationError
from typing import Any, List, Dict


def validate_taeterinnen_details(value: Any) -> None:
    """
    Validate structure of Gewalttat.taeterinnen_details JSONField.
    
    Expected structure:
    [
        {
            "geschlecht": "männlich",
            "verhaeltnis_zur_ratsuchenden_person": "Partner:in"
        },
        ...
    ]
    
    Args:
        value: JSON data to validate
        
    Raises:
        ValidationError: If structure is invalid
    """
    # Must be a list
    if not isinstance(value, list):
        raise ValidationError(
            "taeterinnen_details must be an array/list",
            code='invalid_type'
        )
    
    # Validate each perpetrator entry
    allowed_verhaeltnis = [
        "Unbekannte:r",
        "Bekannte:r",
        "Partner:in",
        "Partner:in ehemalig",
        "Ehepartner:in oder eingetragene:r Lebenspartner:in",
        "andere Familienangehörige",
        "sonstige Personen",
        "keine Angabe"
    ]
    
    for idx, entry in enumerate(value):
        # Must be a dict/object
        if not isinstance(entry, dict):
            raise ValidationError(
                f"Entry {idx} in taeterinnen_details must be an object",
                code='invalid_entry_type'
            )
        
        # Check required keys
        if 'geschlecht' not in entry:
            raise ValidationError(
                f"Entry {idx} missing required field 'geschlecht'",
                code='missing_field'
            )
        
        if 'verhaeltnis_zur_ratsuchenden_person' not in entry:
            raise ValidationError(
                f"Entry {idx} missing required field 'verhaeltnis_zur_ratsuchenden_person'",
                code='missing_field'
            )
        
        # Validate geschlecht is string
        if not isinstance(entry['geschlecht'], str):
            raise ValidationError(
                f"Entry {idx} 'geschlecht' must be a string",
                code='invalid_field_type'
            )
        
        # Validate verhaeltnis is in allowed list
        verhaeltnis = entry['verhaeltnis_zur_ratsuchenden_person']
        if verhaeltnis not in allowed_verhaeltnis:
            raise ValidationError(
                f"Entry {idx} 'verhaeltnis_zur_ratsuchenden_person' must be one of {allowed_verhaeltnis}",
                code='invalid_enum_value'
            )
        
        # No extra keys allowed (strict schema)
        extra_keys = set(entry.keys()) - {'geschlecht', 'verhaeltnis_zur_ratsuchenden_person'}
        if extra_keys:
            raise ValidationError(
                f"Entry {idx} contains unexpected fields: {extra_keys}",
                code='extra_fields'
            )
