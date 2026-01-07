"""
Case management models
Implements Fall (Case) with related demographic data, consultations, and incidents.
Named the landkreis Leipzig Land (-> 3 areas they offer services for, siehe Aufgabenstellung/statistikbogen)
"""
import uuid
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from core.validators.json_validators import validate_taeterinnen_details
from typing import TYPE_CHECKING


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

    def clean(self):
        """Cross-field validation for Fall model."""
        super().clean()
        errors = {}
        
        # Closed cases must have closure date
        if self.ist_abgeschlossen and not self.abschlussdatum:
            errors['abschlussdatum'] = ['Abschlussdatum is required when case is closed']
        
        # informationsquelle "andere Quelle" requires details
        if self.informationsquelle == "andere Quelle":
            if not self.informationsquelle_andere_details or \
               not self.informationsquelle_andere_details.strip():
                errors['informationsquelle_andere_details'] = [
                    'Details required when informationsquelle is "andere Quelle"'
                ]
        
        # Dolmetschung hours must be non-negative
        if self.anzahl_dolmetschungen_stunden < 0:
            errors['anzahl_dolmetschungen_stunden'] = ['Cannot be negative']
        
        if errors:
            raise ValidationError(errors)

    
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
        help_text="Grad der Behinderung (0-100 is the system used in Germany)"
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
    
    def clean(self):
        """
        Cross-field validation for PersonenbezogeneDaten model.
        """
        super().clean()
        errors = {}
        
        # alter_keine_angabe=True requires alter=NULL
        if self.alter_keine_angabe and self.alter is not None:
            errors['alter'] = "Must be empty when 'keine Angabe' is selected"
        
        # grad_der_behinderung requires schwerbehinderung='JA'
        if self.grad_der_behinderung is not None:
            if self.schwerbehinderung != 'JA':  # ← FIXED: Compare to string 'JA', not boolean
                errors['grad_der_behinderung'] = "Only valid when Schwerbehinderung is 'Ja'"
        
        # form_der_behinderung requires schwerbehinderung='JA'
        if self.form_der_behinderung:
            if self.schwerbehinderung != 'JA':  # ← FIXED: Compare to string 'JA'
                errors['form_der_behinderung'] = "Only valid when Schwerbehinderung is 'Ja'"
        
        # staatsangehoerigkeit_land requires staatsangehoerigkeit_deutsch='NICHTDEUTSCH'
        if self.staatsangehoerigkeit_land:
            if self.staatsangehoerigkeit_deutsch == 'DEUTSCH':  # ← FIXED: Compare to string 'DEUTSCH'
                errors['staatsangehoerigkeit_land'] = "Only valid when staatsangehoerigkeit_deutsch is 'nicht deutsch'"
        
        if errors:
            raise ValidationError(errors)

        
        # staatsangehoerigkeit_land requires staatsangehoerigkeit_deutsch = False
        if self.staatsangehoerigkeit_land:
            if self.staatsangehoerigkeit_deutsch is True:
                errors['staatsangehoerigkeit_land'] = [
                    'Only valid when staatsangehoerigkeit_deutsch is False'
                ]
        
        if errors:
            raise ValidationError(errors)

### Beratung and Gewalttat models on new branch

class Beratung(models.Model):
    """
    for individual consultations sessions, linked to Fall
    many-to-one relationship with Fall
    automatically updates Fall.beratungsanzahl and Fall.letzte_beratung on save
    """
    # Durchführungsart choices
    DURCHFUEHRUNGSART_CHOICES = [
        ('PERSOENLICH', 'persönlich'),
        ('VIDEO', 'video'),
        ('TELEFON', 'telefon'),
        ('AUFSUCHEND', 'aufsuchend'),
        ('SCHRIFTLICH', 'schriftlich'),
    ]
    
    # Durchführungsort choices (matches Beratungsstelle locations)
    ORT_CHOICES = [
        ('LEIPZIG_STADT', 'Leipzig Stadt'),
        ('LEIPZIG_LAND', 'Leipzig Land'),
        ('NORDSACHSEN', 'Nordsachsen'),
    ]
    
    # Primary key
    beratung_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Foreign key to Fall (CASCADE delete)
    fall = models.ForeignKey(
        Fall,
        on_delete=models.CASCADE,
        related_name='beratungen'
    )
    
    # Session details
    datum = models.DateField()
    durchfuehrungsart = models.CharField(
        max_length=20,
        choices=DURCHFUEHRUNGSART_CHOICES
    )
    durchfuehrungsort = models.CharField(
        max_length=20,
        choices=ORT_CHOICES
    )
    
    # Notes
    weitere_notizen = models.TextField(blank=True)
    
    class Meta:
        db_table = 'beratung'
        ordering = ['-datum']  # Most recent first
        verbose_name = 'Beratung'
        verbose_name_plural = 'Beratungen'
        indexes = [
            models.Index(fields=['fall', 'datum']),
        ]
    
    def __str__(self):
        return f"Beratung {self.datum} für {self.fall}"
    
    def save(self, *args, **kwargs):
        """
        Override save to update Fall aggregate counters.
        Updates beratungsanzahl and letzte_beratung on parent Fall.
        Also updates letzte_bearbeitung to track case activity.
        """
        # Check if this is a new Beratung (not an update, so we don't double count)
        is_new = self._state.adding
        
        # Save the Beratung first
        super().save(*args, **kwargs)
        
        # Recalculate count only for new records
        if is_new:
            self.fall.beratungsanzahl = self.fall.beratungen.count()  # type: ignore[attr-defined]
            update_fields = ['beratungsanzahl', 'letzte_beratung', 'letzte_bearbeitung']
        else:
            update_fields = ['letzte_beratung', 'letzte_bearbeitung']
        
        # Always update letzte_beratung to most recent date
        latest_beratung = self.fall.beratungen.order_by('-datum').first()  # type: ignore[attr-defined]
        self.fall.letzte_beratung = latest_beratung.datum if latest_beratung else None
        
        # Save Fall with appropriate update_fields
        # letzte_bearbeitung will auto-update because it's in update_fields
        self.fall.save(update_fields=update_fields)


    
    def delete(self, *args, **kwargs) -> tuple[int, dict[str, int]]:
        """
        Override delete to update Fall aggregate counters.
        Returns tuple of (number_deleted, {model_name: count}) per Django convention.
        """
        fall = self.fall
        
        # Delete the Beratung (capture return value)
        deletion_result = super().delete(*args, **kwargs)
        
        # Recalculate aggregates
        fall.beratungsanzahl = fall.beratungen.count()  # type: ignore[attr-defined]
        
        # Update letzte_beratung
        latest_beratung = fall.beratungen.order_by('-datum').first()  # type: ignore[attr-defined]
        fall.letzte_beratung = latest_beratung.datum if latest_beratung else None
        
        # Save Fall with updated aggregates
        fall.save(update_fields=['beratungsanzahl', 'letzte_beratung', 'letzte_bearbeitung'])
        
        # Return Django's expected tuple
        return deletion_result


class Gewalttat(models.Model):
    """
    longest part of this, like 18 fields overall?
    violence incident linked to a Fall.
    One Fall can have multiple Gewalttaten (1:N relationship).
    Many-to-many relationship with GewalttatArt via junction table.
    """
    # Zahl der Vorfälle choices
    VORFAELLE_CHOICES = [
        ('EINMALIG', 'einmalig'),
        ('MEHRERE', 'mehrere'),
        ('GENAUE_ZAHL', 'genaue Zahl'),
        ('KEINE_ANGABE', 'keine Angabe'),
    ]
    
    # Anzahl Täter:innen choices
    TAETERINNEN_ANZAHL_CHOICES = [
        ('1', '1'),
        ('MEHRERE', 'mehrere'),
        ('GENAUE_ZAHL', 'genaue Zahl'),
        ('KEINE_ANGABE', 'keine Angabe'),
    ]
    
    # Tatort choices
    TATORT_CHOICES = [
        ('LEIPZIG', 'Leipzig'),
        ('LEIPZIG_LAND', 'Leipzig Land'),
        ('NORDSACHSEN', 'Nordsachsen'),
        ('SACHSEN', 'Sachsen'),
        ('DEUTSCHLAND', 'Deutschland'),
        ('AUSLAND', 'Ausland'),
        ('AUF_DER_FLUCHT', 'auf der Flucht'),
        ('IM_HERKUNFTSLAND', 'im Herkunftsland'),
        ('KEINE_ANGABE', 'keine Angabe'),
    ]
    
    # Anzeige choices
    ANZEIGE_CHOICES = [
        ('JA', 'Ja'),
        ('NEIN', 'Nein'),
        ('NOCH_NICHT_ENTSCHIEDEN', 'noch nicht entschieden'),
        ('KEINE_ANGABE', 'keine Angabe'),
    ]
    
    # reusable Yes/No/No info choices (for medical care, evidence collection)
    JA_NEIN_KEINE_ANGABE_CHOICES = [
        ('JA', 'Ja'),
        ('NEIN', 'Nein'),
        ('KEINE_ANGABE', 'keine Angabe'),
    ]
    
    # Primary key
    gewalttat_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Foreign key to Fall (CASCADE delete)
    fall = models.ForeignKey(
        Fall,
        on_delete=models.CASCADE,
        related_name='gewalttaten'
    )
    
    # Many-to-many relationship with GewalttatArt via explicit junction table
    gewalttat_arten = models.ManyToManyField(
        'GewalttatArt',
        through='Gewalttat_GewalttatArt',
        related_name='gewalttaten',
        blank=True,
        help_text="Violence types linked via junction table Gewalttat_GewalttatArt"
    )
    
    # Age at time of incident
    alter_zum_zeitpunkt_der_tat = models.IntegerField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(120) # i think thats a reasonable maximum age lol
        ]
    )
    alter_tat_keine_angabe = models.BooleanField(default=False)

    # Time period of incident(s)
    zeitraum_von = models.DateField(null=True, blank=True)
    zeitraum_bis = models.DateField(null=True, blank=True)
    zeitraum_keine_angabe = models.BooleanField(default=False)
    
    # number of incidents
    zahl_der_vorfaelle = models.CharField(
        max_length=20,
        choices=VORFAELLE_CHOICES,
        null=True,
        blank=True
    )
    zahl_der_vorfaelle_genau = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)]
    )
    
    # Number of perpetrators
    anzahl_taeterinnen = models.CharField(
        max_length=20,
        choices=TAETERINNEN_ANZAHL_CHOICES,
        null=True,
        blank=True
    )
    anzahl_taeterinnen_genau = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)]
    )
    
    # Perpetrator details (JSON array)
    taeterinnen_details = models.JSONField(
        default=list,
        blank=True,
        validators=[validate_taeterinnen_details],  # ADD THIS LINE
        help_text="Array of objects with geschlecht and verhaeltnis_zur_ratsuchenden_person"
    )
    
    
    
    # Violence type - linked via M2M junction table (Gewalttat_GewalttatArt)
    # Access via: gewalttat.gewalttat_gewalttatart_set.all()
    
    # Additional details for 'Andere' violence type
    art_der_gewalt_andere_details = models.TextField(blank=True)
    
    # As you see, we refer back to the choices defined above
    # I read that thats how django projects are usually structured
    # Also makes it easier to read and maintain
    # Location of incident
    tatort = models.CharField(
        max_length=30,
        choices=TATORT_CHOICES,
        null=True,
        blank=True
    )
    
    # Legal action
    anzeige = models.CharField(
        max_length=30,
        choices=ANZEIGE_CHOICES,
        null=True,
        blank=True
    )
    
    # Medical response
    medizinische_versorgung = models.CharField(
        max_length=20,
        choices=JA_NEIN_KEINE_ANGABE_CHOICES,
        null=True,
        blank=True
    )
    
    vertrauliche_spurensicherung = models.CharField(
        max_length=20,
        choices=JA_NEIN_KEINE_ANGABE_CHOICES,
        null=True,
        blank=True
    )
    
    # Affected children
    mitbetroffene_kinder = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )
    davon_direkt_betroffen = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )
    
    # Notes
    gewalt_notizen = models.TextField(blank=True)
    
    class Meta:
        db_table = 'gewalttat'
        ordering = ['-zeitraum_von']  # Most recent first
        verbose_name = 'Gewalttat'
        verbose_name_plural = 'Gewalttaten'
        indexes = [
            models.Index(fields=['fall', 'zeitraum_von']),
        ]
    
    def __str__(self):
        if self.zeitraum_von:
            return f"Gewalttat {self.zeitraum_von} - {self.fall}"
        return f"Gewalttat {self.gewalttat_id} - {self.fall}"
    
    def clean(self):
        """Cross-field validation for Gewalttat model."""
        super().clean()
        errors = {}
        
        # zahl_der_vorfaelle = "genaue Zahl" requires zahl_der_vorfaelle_genau
        if self.zahl_der_vorfaelle == "genaue Zahl":
            if self.zahl_der_vorfaelle_genau is None:
                errors['zahl_der_vorfaelle_genau'] = [
                    'Required when "genaue Zahl" is selected'
                ]
        
        # anzahl_taeterinnen = "genaue Zahl" requires anzahl_taeterinnen_genau
        if self.anzahl_taeterinnen == "genaue Zahl":
            if self.anzahl_taeterinnen_genau is None:
                errors['anzahl_taeterinnen_genau'] = [
                    'Required when "genaue Zahl" is selected'
                ]
        
        # zeitraum_von must be before or equal to zeitraum_bis
        if self.zeitraum_von and self.zeitraum_bis:
            if self.zeitraum_von > self.zeitraum_bis:
                errors['zeitraum_von'] = ['Start date cannot be after end date']
        
        # davon_direkt_betroffen cannot exceed mitbetroffene_kinder
        if self.davon_direkt_betroffen > self.mitbetroffene_kinder:
            errors['davon_direkt_betroffen'] = [
                'Cannot exceed total number of affected children'
            ]
        
        # Validate taeterinnen_details JSON structure
        if self.taeterinnen_details:
            try:
                validate_taeterinnen_details(self.taeterinnen_details)
            except ValidationError as e:
                # e.message might be a string or dict, normalize to list
                if isinstance(e.message, str):
                    errors['taeterinnen_details'] = [e.message]
                elif isinstance(e.message, list):
                    errors['taeterinnen_details'] = e.message
                else:
                    errors['taeterinnen_details'] = [str(e.message)]
        
        # alter_tat_keine_angabe = True requires alter_zum_zeitpunkt_der_tat = NULL
        if self.alter_tat_keine_angabe and self.alter_zum_zeitpunkt_der_tat is not None:
            errors['alter_zum_zeitpunkt_der_tat'] = [
                'Must be empty when "keine Angabe" is selected'
            ]
        
        # zeitraum_keine_angabe = True requires both zeitraum fields = NULL
        if self.zeitraum_keine_angabe:
            if self.zeitraum_von is not None or self.zeitraum_bis is not None:
                errors['zeitraum_keine_angabe'] = [
                    'Both zeitraum fields must be empty when "keine Angabe" is selected'
                ]
        
        if errors:
            raise ValidationError(errors)
