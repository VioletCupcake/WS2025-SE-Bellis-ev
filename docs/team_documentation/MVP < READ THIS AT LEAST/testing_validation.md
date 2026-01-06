#### Testing Phase 2 A - Validation /validator




>>> # Test PersonenbezogeneDaten validation
>>> from core.models import PersonenbezogeneDaten, Fall
>>> from django.core.exceptions import ValidationError
>>> 
>>> # Should raise ValidationError
>>> try:
...     p = PersonenbezogeneDaten(
...         alter=25,
...         alter_keine_angabe=True  # Conflict!
...     )
...     p.clean()  # This should raise ValidationError
... except ValidationError as e:
...     print("✓ Validation caught error:", e)
... 
✓ Validation caught error: {'alter': ['Must be empty when "keine Angabe" is selected']}

## Coniditional field validation works

>>> from core.models import Gewalttat, Fall
>>> from datetime import date
>>> from django.core.exceptions import ValidationError
>>> 
>>> try:
...     g = Gewalttat(
...         zeitraum_von=date(2025, 6, 1),
...         zeitraum_bis=date(2025, 1, 1)  # Before start date!
...     )
...     g.clean()
... except ValidationError as e:
...     print("✓ Date range validation works:", e)
... 
✓ Date range validation works: {'zeitraum_von': ['Start date cannot be after end date']}




>>> try:
...     g = Gewalttat(
...         taeterinnen_details=[
...             {
...                 "geschlecht": "männlich",
...                 "verhaeltnis_zur_ratsuchenden_person": "INVALID_VALUE"  # Not in allowed list
...             }
...         ]
...     )
...     g.clean()
... except ValidationError as e:
...     print("✓ JSON validation works:", e)
... 
✓ JSON validation works: {'taeterinnen_details': ["Entry 0 'verhaeltnis_zur_ratsuchenden_person' must be one of ['Unbekannte:r', 'Bekannte:r', 'Partner:in', 'Partner:in ehemalig', 'Ehepartner:in oder eingetragene:r Lebenspartner:in', 'andere Familienangehörige', 'sonstige Personen', 'keine Angabe']"]}