============================================================================
## SE_B-EV_2025 – MVP UML CLASS DIAGRAM (DJANGO MAPPED) --> NOT REALLY UML ANYMORE NOW IS IT???
## Minimum Viable Product - Django Implementation Specification
============================================================================
## DJANGO CONVENTIONS
## All models inherit from: models.Model
## Field types: CharField, IntegerField, ForeignKey, ManyToManyField, etc.
## Managers: Custom QuerySet methods on .objects
## Methods: Instance methods for business logic
============================================================================


============================================================================
## 01 USER & PERMISSION SYSTEM (models/user_models.py)
============================================================================


## User (extends models.Model)
## Django: AbstractUser or custom model with AUTH_USER_MODEL
User(models.Model):
- user_id : UUIDField(primary_key=True, default=uuid.uuid4)
- username : CharField(max_length=150, unique=True)
- email : EmailField(unique=True)
- password : CharField(max_length=128)  ## Django hashed automatically
- role : ForeignKey(Role, on_delete=models.RESTRICT, related_name='users')
- is_active : BooleanField(default=True)
- created_at : DateTimeField(auto_now_add=True)
+ login(username: str, password: str) : Session  ## Uses django.contrib.auth
+ logout(session_id: str) : void
+ change_password(old_password: str, new_password: str) : bool
+ __str__() : str  ## Returns username


## Session (extends models.Model)
## Django: Can use django.contrib.sessions or custom model
Session(models.Model):
- session_id : CharField(primary_key=True, max_length=40)
- user : ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
- start_time : DateTimeField(auto_now_add=True)
- last_activity : DateTimeField(auto_now=True)
- is_active : BooleanField(default=True)
+ extend() : void
+ terminate() : void
+ __str__() : str  ## Returns f"Session for {user.username}"


## Role (extends models.Model)
## Django: Simple model with choices for name field
Role(models.Model):
- role_id : UUIDField(primary_key=True, default=uuid.uuid4)
- name : CharField(max_length=20, choices=ROLE_CHOICES, unique=True)
    ## ROLE_CHOICES = [('BASIS', 'Basis'), ('ERWEITERT', 'Erweitert'), ('ADMIN', 'Administrator')]
- description : TextField(blank=True)
+ is_authorized(permission: str) : bool
+ __str__() : str  ## Returns name


## PermissionSet (extends models.Model)
## Django: OneToOneField to Role
PermissionSet(models.Model):
- permission_set_id : UUIDField(primary_key=True, default=uuid.uuid4)
- role : OneToOneField(Role, on_delete=models.CASCADE, related_name='permissions')
- can_view_cases : BooleanField(default=True)
- can_edit_cases : BooleanField(default=False)
- can_delete_cases : BooleanField(default=False)
- can_manage_reference_data : BooleanField(default=False)
- can_manage_users : BooleanField(default=False)
- can_assign_roles : BooleanField(default=False)
+ validate() : bool
+ __str__() : str  ## Returns f"Permissions for {role.name}"


============================================================================
## 02 CASE MANAGEMENT (models/fall_models.py)
============================================================================


## Fall (extends models.Model)
## Django: Core model with related manager for beratungen, gewalttaten
Fall(models.Model):
- fall_id : UUIDField(primary_key=True, default=uuid.uuid4)
- alias : CharField(max_length=50, unique=True, db_index=True)
- zustaendige_beratungsstelle : CharField(max_length=20, choices=BERATUNGSSTELLE_CHOICES)
    ## CHOICES: 'LEIPZIG_STADT', 'LEIPZIG_LAND', 'NORDSACHSEN'
- erstellungsdatum : DateField(auto_now_add=True)
- letzte_bearbeitung : DateTimeField(auto_now=True)
- bearbeitet_von : ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='bearbeitete_faelle')
- status : CharField(max_length=20, choices=STATUS_CHOICES, default='AKTIV')
    ## CHOICES: 'AKTIV', 'ARCHIVIERT'
- ist_vollstaendig : BooleanField(default=False)
- ist_abgeschlossen : BooleanField(default=False)
- abschlussdatum : DateTimeField(null=True, blank=True)
- beratungsanzahl : IntegerField(default=0)
- letzte_beratung : DateField(null=True, blank=True)
- informationsquelle : CharField(max_length=20, choices=INFO_QUELLE_CHOICES)
    ## CHOICES: 'POLIZEI', 'KONTAKTE', 'INTERNET', 'AEMTER', 'ANDERE'
- informationsquelle_andere : TextField(blank=True)
- anzahl_dolmetschungen_stunden : FloatField(default=0.0)
- dolmetschung_sprachen : TextField(blank=True)
- weitere_notizen : TextField(blank=True)
+ save(*args, **kwargs) : void  ## Override to update beratungsanzahl
+ close() : void  ## Sets ist_abgeschlossen, abschlussdatum
+ __str__() : str  ## Returns alias
## Meta:
    ordering = ['-erstellungsdatum']
    indexes = [models.Index(fields=['alias', 'erstellungsdatum'])]


## PersonenbezogeneDaten (extends models.Model)
## Django: OneToOneField to Fall with CASCADE delete
PersonenbezogeneDaten(models.Model):
- personenbezogene_daten_id : UUIDField(primary_key=True, default=uuid.uuid4)
- fall : OneToOneField(Fall, on_delete=models.CASCADE, related_name='personenbezogene_daten')
- rolle_der_ratsuchenden_person : CharField(max_length=20, choices=ROLLE_CHOICES)
    ## CHOICES: 'BETROFFENE', 'ANGEHOERIGE', 'FACHKRAFT'
- alter : IntegerField(null=True, blank=True)
- alter_keine_angabe : BooleanField(default=False)
- geschlechtsidentitaet : CharField(max_length=20, choices=GESCHLECHT_CHOICES)
    ## CHOICES: 'CIS_W', 'CIS_M', 'TRANS_W', 'TRANS_M', 'NB', 'INTER', 'AGENDER', 'DIVERS', 'KEINE_ANGABE'
- sexualitaet : CharField(max_length=20, choices=SEXUALITAET_CHOICES)
- wohnort : CharField(max_length=20, choices=WOHNORT_CHOICES)
- wohnort_details : TextField(blank=True)
- staatsangehoerigkeit_deutsch : BooleanField(default=True)
- staatsangehoerigkeit_land : CharField(max_length=100, blank=True)
- berufliche_situation : CharField(max_length=30, choices=BERUF_CHOICES)
- schwerbehinderung : BooleanField(default=False)
- form_der_behinderung : CharField(max_length=20, choices=BEHINDERUNG_CHOICES, blank=True)
- grad_der_behinderung : IntegerField(null=True, blank=True)
- weitere_notizen : TextField(blank=True)
+ __str__() : str  ## Returns f"Daten für {fall.alias}"


## Beratung (extends models.Model)
## Django: ForeignKey to Fall with CASCADE delete
Beratung(models.Model):
- beratung_id : UUIDField(primary_key=True, default=uuid.uuid4)
- fall : ForeignKey(Fall, on_delete=models.CASCADE, related_name='beratungen')
- datum : DateField()
- durchfuehrungsart : CharField(max_length=20, choices=DURCHFUEHRUNGSART_CHOICES)
    ## CHOICES: 'PERSOENLICH', 'VIDEO', 'TELEFON', 'AUFSUCHEND', 'SCHRIFTLICH'
- durchfuehrungsort : CharField(max_length=20, choices=ORT_CHOICES)
- weitere_notizen : TextField(blank=True)
+ save(*args, **kwargs) : void  ## Override to update Fall.beratungsanzahl
+ __str__() : str  ## Returns f"Beratung {datum} für {fall.alias}"
## Meta:
    ordering = ['-datum']


## Gewalttat (extends models.Model)
## Django: ForeignKey to Fall, JSONField for taeterinnen_details
Gewalttat(models.Model):
- gewalttat_id : UUIDField(primary_key=True, default=uuid.uuid4)
- fall : ForeignKey(Fall, on_delete=models.CASCADE, related_name='gewalttaten')
- alter_zum_zeitpunkt_der_tat : IntegerField(null=True, blank=True)
- alter_keine_angabe : BooleanField(default=False)
- zeitraum_von : DateField(null=True, blank=True)
- zeitraum_bis : DateField(null=True, blank=True)
- zeitraum_keine_angabe : BooleanField(default=False)
- zahl_der_vorfaelle : CharField(max_length=20, choices=VORFAELLE_CHOICES)
- zahl_der_vorfaelle_genau : IntegerField(null=True, blank=True)
- anzahl_taeterinnen : CharField(max_length=20, choices=TAETER_ANZAHL_CHOICES)
- anzahl_taeterinnen_genau : IntegerField(null=True, blank=True)
- taeterinnen_details : JSONField(default=list)  ## [{geschlecht: str, verhaeltnis: str}]
- tatort : CharField(max_length=20, choices=TATORT_CHOICES)
- anzeige : CharField(max_length=20, choices=ANZEIGE_CHOICES)
- medizinische_versorgung : CharField(max_length=20, choices=JA_NEIN_KA_CHOICES)
- vertrauliche_spurensicherung : CharField(max_length=20, choices=JA_NEIN_KA_CHOICES)
- mitbetroffene_kinder : IntegerField(default=0)
- davon_direkt_betroffen : IntegerField(default=0)
- weitere_notizen : TextField(blank=True)
+ add_taeterin(geschlecht: str, verhaeltnis: str) : void
+ __str__() : str  ## Returns f"Gewalttat für {fall.alias}"


============================================================================
## 03 REFERENCE DATA (models/reference_models.py)
============================================================================


## GewalttatArt (extends models.Model)
## Django: Self-referential ForeignKey for hierarchy
GewalttatArt(models.Model):
- art_id : UUIDField(primary_key=True, default=uuid.uuid4)
- name : CharField(max_length=100, unique=True)
- ist_unterkategorie : BooleanField(default=False)
- hauptkategorie : ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='unterkategorien')
- beschreibung : TextField(blank=True)
+ __str__() : str  ## Returns name
## Meta:
    ordering = ['name']


## Gewalttat_GewalttatArt (extends models.Model)
## Django: Junction table with compound primary key via unique_together
Gewalttat_GewalttatArt(models.Model):
- gewalttat : ForeignKey(Gewalttat, on_delete=models.CASCADE)
- art : ForeignKey(GewalttatArt, on_delete=models.CASCADE)
- andere_details : TextField(blank=True)
+ __str__() : str  ## Returns f"{gewalttat.fall.alias} - {art.name}"
## Meta:
    unique_together = [['gewalttat', 'art']]


## FolgenDerGewalt (extends models.Model)
## Django: Self-referential ForeignKey for hierarchy
FolgenDerGewalt(models.Model):
- folge_id : UUIDField(primary_key=True, default=uuid.uuid4)
- name : CharField(max_length=100, unique=True)
- kategorie : CharField(max_length=20, choices=FOLGEN_KATEGORIE_CHOICES)
    ## CHOICES: 'PSYCHISCH', 'KOERPERLICH', 'DAUERHAFT', 'FINANZIELL'
- ist_unterkategorie : BooleanField(default=False)
- hauptkategorie : ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='unterkategorien')
- beschreibung : TextField(blank=True)
+ __str__() : str  ## Returns name
## Meta:
    ordering = ['kategorie', 'name']


## Fall_FolgenDerGewalt (extends models.Model)
## Django: Junction table with additional field
Fall_FolgenDerGewalt(models.Model):
- fall : ForeignKey(Fall, on_delete=models.CASCADE, related_name='folgen_relations')
- folge : ForeignKey(FolgenDerGewalt, on_delete=models.CASCADE)
- weitere_informationen : TextField(blank=True)
+ __str__() : str  ## Returns f"{fall.alias} - {folge.name}"
## Meta:
    unique_together = [['fall', 'folge']]


============================================================================
## 04 VALIDATION SYSTEM (services/validation_service.py)
============================================================================


## ValidationService
## Django: Standalone service class (not a model)
ValidationService:
+ validate_input(input_data: dict, field_name: str, field_type: str) : ValidationResult
+ validate_password(password: str) : bool  ## Uses django.contrib.auth.password_validation
+ validate_date(date_string: str) : bool
+ validate_number(number_string: str) : bool
+ validate_enum(value: str, allowed_values: list) : bool


## ValidationResult
## Django: Dataclass or simple class (not a model)
ValidationResult:
- is_valid : bool
- error_messages : list[str]
+ add_error(error: str) : void
+ get_summary() : str


============================================================================
## 05 MANAGER CLASSES (managers/)
============================================================================


## FallManager
## Django: Custom manager or service class
FallManager:
+ create_fall(data: dict) : Fall  ## Uses transaction.atomic()
+ update_fall(fall_id: UUID, data: dict) : Fall
+ delete_fall(fall_id: UUID) : void  ## Sets status=ARCHIVIERT
+ add_beratung(fall_id: UUID, data: dict) : Beratung
+ add_gewalttat(fall_id: UUID, data: dict) : Gewalttat
+ close_fall(fall_id: UUID) : void
+ search_by_alias(alias: str) : Fall  ## Uses Fall.objects.get()
+ search_by_date_range(from_date: date, to_date: date) : QuerySet[Fall]


## SessionManager
## Django: Custom manager or use django.contrib.sessions
SessionManager:
- active_sessions : dict[str, Session]
+ create_session(user: User) : Session
+ destroy_session(session_id: str) : void
+ validate_session(session_id: str) : bool
+ cleanup_expired() : int  ## Uses Session.objects.filter()


============================================================================
## 06 DJANGO-SPECIFIC RELATIONSHIPS
============================================================================


## CASCADE DELETE
Fall 1 --CASCADE--> 1 PersonenbezogeneDaten
Fall 1 --CASCADE--> * Beratung
Fall 1 --CASCADE--> * Gewalttat
Fall 1 --CASCADE--> * Fall_FolgenDerGewalt
Gewalttat 1 --CASCADE--> * Gewalttat_GewalttatArt
User 1 --CASCADE--> * Session

## SET NULL
User 1 --SET_NULL--> * Fall (bearbeitet_von)

## RESTRICT
Role 1 --RESTRICT--> * User
Role 1 --RESTRICT--> 1 PermissionSet

## SELF-REFERENTIAL
GewalttatArt 1 --SET_NULL--> * GewalttatArt (hauptkategorie)
FolgenDerGewalt 1 --SET_NULL--> * FolgenDerGewalt (hauptkategorie)


============================================================================
## 07 DJANGO FIELD TYPE MAPPING REFERENCE
============================================================================

UUIDField           → Primary keys (auto-generated)
CharField           → Short text with max_length
TextField           → Long text (no length limit)
EmailField          → Email validation
IntegerField        → Integers
FloatField          → Decimals
BooleanField        → True/False
DateField           → Date only
DateTimeField       → Date + time
JSONField           → JSON data (requires PostgreSQL)
ForeignKey          → One-to-many relationship
OneToOneField       → One-to-one relationship
ManyToManyField     → Many-to-many (auto junction table)


============================================================================
## END OF DJANGO-MAPPED MVP UML CLASS DIAGRAM
============================================================================
