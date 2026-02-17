
"""
Models for Statistics feature.
"""
import uuid
from django.db import models
from django.conf import settings

class StatistikPreset(models.Model):
    """
    Saved filter configuration for statistics dashboard.
    Can be personal (user-specific) or global (visible to all).
    """
    preset_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    name = models.CharField(max_length=100)
    beschreibung = models.TextField(blank=True)
    
    # JSON configuration for filters
    # Structure: {
    #   "date_from": "YYYY-MM-DD",
    #   "date_to": "YYYY-MM-DD",
    #   "beratungsstellen": ["FBS_1", ...],
    #   "modules": ["personen", "beratung", ...]
    # }
    filter_config = models.JSONField(default=dict)
    
    # Ownership and visibility
    erstellt_von = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='statistik_presets',
        null=True, # Null for system presets if needed, though system presets essentially belong to "system"
        blank=True
    )
    
    ist_global = models.BooleanField(
        default=False,
        help_text="Visible to all users if True"
    )
    
    ist_system_preset = models.BooleanField(
        default=False,
        editable=False,
        help_text="System-provided preset, cannot be deleted"
    )
    
    erstellungsdatum = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'statistik_preset'
        ordering = ['name']
        verbose_name = 'Statistik Preset'
        verbose_name_plural = 'Statistik Presets'
    
    def __str__(self):
        return self.name
