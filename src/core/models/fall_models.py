"""
Case management models
Implements Fall (Case) with related demographic data, consultations, and incidents.
Named the landkreis Leipzig Land (-> 3 areas they offer services for, siehe Aufgabenstellung/statistikbogen)
"""
import uuid
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class Fall(models.Model):
    """
    Core case entity.
    Tracks case metadata, status, and aggregate counters.
    Does NOT contain personal demographic data (stored in PersonenbezogeneDaten).
    """
    # Beratungsstelle choices, changed naming and short codes to match my initial concept and statiskbogen
    BERATUNGSSTELLE_CHOICES = [
        ('FBS_1_LE', 'Fachberatungsstelle für queere Betroffene von sexualisierter Gewalt in der Stadt Leipzig'),
        ('FBS_2_LKNSA', 'Fachberatung gegen sexualisierte Gewalt im Landkreis Nordsachsen'),
        ('FBS_3_LKLE', 'Fachberatung gegen sexualisierte Gewalt im Landkreis Leipzig'),
    ]
    
    # Status choices, Archived = soft deleted, relic of before we had hard delete
    STATUS_CHOICES = [
        ('AKTIV', 'Aktiv'),
        ('ARCHIVIERT', 'Archiviert'),
    ]
    
    # Informationsquelle choices (from weitere_daten section, moved up here because its meta data and short)
    INFO_QUELLE_CHOICES = [
        ('POLIZEI', 'Selbstmeldungen über Polizei'),
        ('PRIVATE_KONTAKTE', 'Private Kontakte'),
        ('BERATUNGSSTELLEN', 'Beratungsstellen'),
        ('INTERNET', 'Internet'),
        ('AEMTER', 'Ämter'),
        ('GESUNDHEITSWESEN', 'Gesundheitswesen (Arzt/Ärztin)'),
        ('RECHTSANWAELTE', 'Rechtsanwälte/-anwältinnen'),
        ('ANDERE', 'andere Quelle'),
        ('KEINE_ANGABE', 'keine Angabe'),
    ]
    
    # Primary key
    fall_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Core identification - zustaendige_beratungsstelle from beratungen_gesamt
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
    
    # Aggregate counters (from beratungen_gesamt)
    beratungsanzahl = models.IntegerField(default=0)
    letzte_beratung = models.DateField(null=True, blank=True)
    
    # Weitere Daten section - Information source
    informationsquelle = models.CharField(
        max_length=30,
        choices=INFO_QUELLE_CHOICES,
        null=True,
        blank=True
    )
    informationsquelle_andere_details = models.TextField(blank=True)
    
    # Weitere Daten section - Interpreter usage
    # if 0.0 > no interpreter used, otherwise used to show hours, language can be entered
    anzahl_dolmetschungen_stunden = models.FloatField(default=0.0)
    dolmetschung_sprachen = models.TextField(blank=True)
    
    # General notes
    weitere_notizen = models.TextField(blank=True)
    
    class Meta:
        db_table = 'fall'
        ordering = ['-erstellungsdatum']
        indexes = [
            models.Index(fields=['erstellungsdatum']),
            models.Index(fields=['zustaendige_beratungsstelle']),
        ]
        verbose_name = 'Fall'
        verbose_name_plural = 'Fälle'

    
    def __str__(self):
        """String representation using alias from PersonenbezogeneDaten if exists."""
        if hasattr(self, 'personenbezogene_daten'):
            return self.personenbezogene_daten.alias  # type: ignore[attr-defined]
        return f"Fall {self.fall_id}"

    
    def close(self):
        """Mark case as closed."""
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
        Permanent deletion for DSGVO compliance. Should be in here regardless
        also good since we took autodelete out of the mvp
        
        Cascades to:
        - PersonenbezogeneDaten (1:1)
        - Beratung records (1:N, future)
        - Gewalttat records (1:N, future)
        - Fall_FolgenDerGewalt junction entries (N:M, future)
        
        WARNING: This action is irreversible.
        """
        self.delete()

class PersonenbezogeneDaten(models.Model):
    """
    Personal demographic data linked 1:1 to Fall.
    Separated for privacy by design ->> easier to audit/encrypt/delete.
    Also just easier to manage separately
    Contains alias and all demographic information.
    """
    # Rolle choices
    ROLLE_CHOICES = [
        ('BETROFFENE', 'Betroffene:r'),
        ('ANGEHOERIGE', 'Angehörige:r'),
        ('FACHKRAFT', 'Fachkraft'),
    ]
    
    # Geschlechtsidentität choices
    GESCHLECHT_CHOICES = [
        ('CIS_W', 'cis weiblich'),
        ('CIS_M', 'cis männlich'),
        ('TRANS_W', 'trans weiblich'),
        ('TRANS_M', 'trans männlich'),
        ('TRANS_NB', 'trans nicht binär'),
        ('INTER', 'inter'),
        ('AGENDER', 'agender'),
        ('DIVERS', 'divers'),
        ('KEINE_ANGABE', 'keine Angabe'),
    ]
    
    # Sexualität choices
    SEXUALITAET_CHOICES = [
        ('LESBISCH', 'lesbisch'),
        ('SCHWUL', 'schwul'),
        ('BISEXUELL', 'bisexuell'),
        ('ASEXUELL', 'asexuell'),
        ('HETEROSEXUELL', 'heterosexuell'),
        ('KEINE_ANGABE', 'keine Angabe'),
    ]
    
    # Wohnort choices
    WOHNORT_CHOICES = [
        ('LEIPZIG_STADT', 'Leipzig Stadt'),
        ('LEIPZIG_LAND', 'Leipzig Land'),
        ('NORDSACHSEN', 'Nordsachsen'),
        ('SACHSEN', 'Sachsen'),
        ('DEUTSCHLAND', 'Deutschland'),
        ('ANDERE', 'andere'),
        ('KEINE_ANGABE', 'keine Angabe'),
    ]
    
    # Staatsangehörigkeit choices
    STAATSANGEHOERIGKEIT_CHOICES = [
        ('DEUTSCH', 'deutsch'),
        ('NICHT_DEUTSCH', 'nicht deutsch'),
    ]
    
    # Berufliche Situation choices
    BERUF_CHOICES = [
        ('ARBEITSLOS', 'arbeitslos'),
        ('STUDIEREND', 'studierend'),
        ('BERUFSTAETIG', 'berufstätig'),
        ('BERENTET', 'berentet'),
        ('AZUBI', 'Azubi'),
        ('BERUFSUNFAEHIG', 'berufsunfähig'),
        ('KEINE_ANGABE', 'keine Angabe'),
    ]
    
    # Schwerbehinderung choices
    SCHWERBEHINDERUNG_CHOICES = [
        ('JA', 'Ja'),
        ('NEIN', 'Nein'),
    ]
    
    # Form der Behinderung choices
    BEHINDERUNG_CHOICES = [
        ('KOGNITIV', 'kognitiv'),
        ('KOERPERLICH', 'körperlich'),
    ]
    
    # Primary key
    personenbezogene_daten_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # 1:1 relationship with Fall (CASCADE delete)
    fall = models.OneToOneField(
        Fall,
        on_delete=models.CASCADE,
        related_name='personenbezogene_daten'
    )
    
    # Alias - unique identifier moved from Fall
    alias = models.CharField(max_length=64, unique=True, db_index=True)
    
    # Core demographic data
    rolle_der_ratsuchenden_person = models.CharField(
        max_length=20,
        choices=ROLLE_CHOICES
    )
    
    # Age with explicit "no information" flag
    alter = models.IntegerField(null=True, blank=True)
    alter_keine_angabe = models.BooleanField(default=False)
    
    # Gender identity and sexuality
    geschlechtsidentitaet = models.CharField(
        max_length=20,
        choices=GESCHLECHT_CHOICES,
        null=True,
        blank=True
    )
    sexualitaet = models.CharField(
        max_length=20,
        choices=SEXUALITAET_CHOICES,
        null=True,
        blank=True
    )
    
    # Location
    wohnort = models.CharField(
        max_length=20,
        choices=WOHNORT_CHOICES,
        null=True,
        blank=True
    )
    wohnort_details = models.TextField(blank=True)
    
    # Nationality
    staatsangehoerigkeit_deutsch = models.CharField(
        max_length=20,
        choices=STAATSANGEHOERIGKEIT_CHOICES,
        null=True,
        blank=True
    )
    staatsangehoerigkeit_land = models.CharField(max_length=100, blank=True)
    
    # Professional situation
    berufliche_situation = models.CharField(
        max_length=30,
        choices=BERUF_CHOICES,
        null=True,
        blank=True
    )
    
    # Disability information
    schwerbehinderung = models.CharField(
        max_length=10,
        choices=SCHWERBEHINDERUNG_CHOICES,
        null=True,
        blank=True
    )
    form_der_behinderung = models.CharField(
        max_length=20,
        choices=BEHINDERUNG_CHOICES,
        blank=True
    )
    grad_der_behinderung = models.IntegerField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(0, message="GdB muss mindestens 0 sein"),
            MaxValueValidator(100, message="GdB darf höchstens 100 sein")
        ],
        help_text="Grad der Behinderung (0-100, German system)"
    )
    # Form & Grad nur visible if Schwerbehinderung == 'JA'
    
    # Notes
    personenbezogene_notizen = models.TextField(blank=True)
    
    class Meta:
        db_table = 'personenbezogene_daten'
        verbose_name = 'Personenbezogene Daten'
        verbose_name_plural = 'Personenbezogene Daten'
    
    def __str__(self):
        return f"Daten für {self.alias}"
