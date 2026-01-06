"""Reference data model definitions.
create GewalttatArt and FolgenDerGewalt here

User with ERWEITERT Role should be able to edit/extend these via the admin interface later"""

import uuid
from django.db import models


class GewalttatArt(models.Model):
    """
    Violence type reference data with hierarchical categories.
    Main categories (hauptkategorie=NULL) contain subcategories.
    ERWEITERT role can add new entries via admin.
    """
    # Primary key
    art_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Name must be unique across all categories and subcategories
    name = models.CharField(max_length=100, unique=True)
    
    # Hierarchy support
    ist_unterkategorie = models.BooleanField(default=False)
    hauptkategorie = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='unterkategorien'
    )
    
    # Description for clarification
    beschreibung = models.TextField(blank=True)
    
    class Meta:
        db_table = 'gewalttat_art'
        ordering = ['name']
        verbose_name = 'Gewalttat Art'
        verbose_name_plural = 'Gewalttat Arten'
    
    def __str__(self):
        return self.name


class FolgenDerGewalt(models.Model):
    """
    Consequence type reference data with hierarchical categories.
    Categorized by type: psychisch, körperlich, dauerhaft, finanziell.
    ERWEITERT role can add new entries via admin.
    """
    # Category choices
    FOLGEN_KATEGORIE_CHOICES = [
        ('PSYCHISCH', 'Psychisch'),
        ('KOERPERLICH', 'Körperlich'),
        ('DAUERHAFT', 'Dauerhaft'),
        ('FINANZIELL', 'Finanziell'),
    ]
    
    # Primary key
    folge_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Name must be unique
    name = models.CharField(max_length=100, unique=True)
    
    # Category classification
    kategorie = models.CharField(
        max_length=20,
        choices=FOLGEN_KATEGORIE_CHOICES
    )
    
    # Hierarchy support
    ist_unterkategorie = models.BooleanField(default=False)
    hauptkategorie = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='unterkategorien'
    )
    
    # Description for clarification
    beschreibung = models.TextField(blank=True)
    
    class Meta:
        db_table = 'folgen_der_gewalt'
        ordering = ['kategorie', 'name']
        verbose_name = 'Folge der Gewalt'
        verbose_name_plural = 'Folgen der Gewalt'
    
    def __str__(self):
        return self.name


class Fall_FolgenDerGewalt(models.Model):
    """
    Junction table linking cases to consequence types.
    Supports many-to-many: one Fall can have multiple FolgenDerGewalt.
    Allows additional information per consequence.
    """
    # Foreign keys
    fall = models.ForeignKey(
        'Fall',
        on_delete=models.CASCADE,
        related_name='folgen_relations'
    )
    folge = models.ForeignKey(
        FolgenDerGewalt,
        on_delete=models.CASCADE
    )
    
    # Additional information about this consequence
    weitere_informationen = models.TextField(blank=True)
    
    class Meta:
        db_table = 'fall_folgen_der_gewalt'
        unique_together = [['fall', 'folge']]  # Prevent duplicate links
        verbose_name = 'Fall-Folge Verknüpfung'
        verbose_name_plural = 'Fall-Folge Verknüpfungen'
    
    def __str__(self):
        return f"{self.fall} - {self.folge.name}"  # type: ignore[attr-defined]


# NOTE: Gewalttat_GewalttatArt junction table will be created in next migration
# when Gewalttat model is implemented (Phase 1B.3)
# NOTE: Here it is, woop woop

class Gewalttat_GewalttatArt(models.Model):
    """
    Junction table linking violence incidents to violence types.
    Supports many-to-many: one Gewalttat can have multiple GewalttatArt.
    Allows additional details per link (e.g., 'Andere' free text).
    """
    # Foreign keys
    gewalttat = models.ForeignKey(
        'Gewalttat',  # String reference - Gewalttat in fall_models.py
        on_delete=models.CASCADE
    )
    art = models.ForeignKey(
        GewalttatArt,
        on_delete=models.CASCADE
    )
    
    # Additional details (e.g., for 'Andere' selection)
    andere_details = models.TextField(blank=True)
    
    class Meta:
        db_table = 'gewalttat_gewalttat_art'
        unique_together = [['gewalttat', 'art']]  # Prevent duplicate links
        verbose_name = 'Gewalttat-Art Verknüpfung'
        verbose_name_plural = 'Gewalttat-Art Verknüpfungen'
    
    def __str__(self):
        return f"{self.gewalttat.fall} - {self.art.name}"  # type: ignore[attr-defined]
