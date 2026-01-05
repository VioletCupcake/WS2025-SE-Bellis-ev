"""
Case management models
Implements Fall (Case) with related demographic data, consultations, and incidents.
Named the landkreis Leipzig Land (-> 3 areas they offer services for, siehe Aufgabenstellung/statistikbogen)
"""
import uuid
from django.db import models
from django.conf import settings


class Fall(models.Model):
    """
    Core case entity.
    Tracks case metadata, status, and aggregate counters.
    """
    # Beratungsstelle choices, unsure if this is Anfrage only
    BERATUNGSSTELLE_CHOICES = [
        ('LEIPZIG_STADT', 'Leipzig Stadt'),
        ('LEIPZIG_LAND', 'Leipzig Land'),
        ('NORDSACHSEN', 'Nordsachsen'),
    ]
    
    # Status choices
    STATUS_CHOICES = [
        ('AKTIV', 'Aktiv'),
        ('ARCHIVIERT', 'Archiviert'), #aktuell nur archivierung, sollten hard delete noch implementieren
    ]
    
    
    # Primary key
    fall_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Core identification
    alias = models.CharField(max_length=50, unique=True, db_index=True)
    zustaendige_beratungsstelle = models.CharField(
        max_length=20,
        choices=BERATUNGSSTELLE_CHOICES
    )
    
    # Timestamps
    erstellungsdatum = models.DateField(auto_now_add=True)
    letzte_bearbeitung = models.DateTimeField(auto_now=True)
    bearbeitet_von = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='bearbeitete_faelle'
    )
    
    # Status tracking
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='AKTIV'
    )
    ist_vollstaendig = models.BooleanField(default=False)
    ist_abgeschlossen = models.BooleanField(default=False)
    abschlussdatum = models.DateTimeField(null=True, blank=True)
    
    # Aggregate counters (denormalized for performance)
    beratungsanzahl = models.IntegerField(default=0)
    letzte_beratung = models.DateField(null=True, blank=True)

    
    # Additional services
    anzahl_dolmetschungen_stunden = models.FloatField(default=0.0)
    dolmetschung_sprachen = models.TextField(blank=True)
    weitere_notizen = models.TextField(blank=True)
    
    class Meta:
        db_table = 'fall'
        ordering = ['-erstellungsdatum']
        indexes = [
            models.Index(fields=['alias', 'erstellungsdatum']),
        ]
        verbose_name = 'Fall'
        verbose_name_plural = 'Fälle'
    
    def __str__(self):
        return self.alias
    
    
    def close(self):
        """Mark case as closed (soft delete alternative)."""
        from django.utils import timezone
        self.ist_abgeschlossen = True
        self.abschlussdatum = timezone.now()
        self.save()
    
    def archive(self):
        """Soft delete - mark as archived."""
        self.status = 'ARCHIVIERT'
        self.save()
    
    def hard_delete(self):
        """
        Permanent deletion for DSGVO compliance.
        
        Cascades to:
        - PersonenbezogeneDaten (1:1)
        - Beratung records (1:N)
        - Gewalttat records (1:N)
        - Fall_FolgenDerGewalt junction entries (N:M)
        
        WARNING: This action is irreversible.
        """
        # Django's delete() method triggers CASCADE
        self.delete()
