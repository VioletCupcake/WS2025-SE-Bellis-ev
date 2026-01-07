
>>> from core.models import Fall, PersonenbezogeneDaten, Role
>>> 
>>> # Test Fall creation
>>> fall = Fall.objects.create(
...     zustaendige_beratungsstelle='FBS_1_LE',
...     status='AKTIV'
... )
.fall_id}")>>> print(f"Fall created: {fall.fall_id}")
Fall created: d3c56e30-8850-46a7-b659-4576910df472

## Fall Creation works

>>> personen_daten = PersonenbezogeneDaten.objects.create(
...     fall=fall,
...     alias='TEST_001',
...     rolle_der_ratsuchenden_person='BETROFFENE',
...     alter=30
... )
nen_daten.alias}")>>> print(f"PersonenbezogeneDaten created: {personen_daten.alias}")
PersonenbezogeneDaten created: TEST_001
>>> print(f"Fall __str__: {fall}")  # Should print "TEST_001"
Fall __str__: TEST_001

### creating personenbez. daten works

>>> fall.delete()
neDaten should be cascade-deleted")(2, {'core.PersonenbezogeneDaten': 1, 'core.Fall': 1})
>>> print("Fall deleted")
Fall deleted

# delete works

>>> count = PersonenbezogeneDaten.objects.filter(alias='TEST_001').count()
 count (should be 0): {count}")>>> print(f"PersonenbezogeneDaten count (should be 0): {count}")
PersonenbezogeneDaten count (should be 0): 0

## also cascades i guess?



=================== MORE TESTING ================

>>> from core.models import Fall, PersonenbezogeneDaten, Beratung
>>> print(Beratung)
<class 'core.models.fall_models.Beratung'>
>>> print(Beratung._meta.db_table)
beratung

## great i fixed the error earlie where Beratung wasnt proerply integrated inti __init__.py

>>> from core.models import Fall, PersonenbezogeneDaten, Beratung
>>> from datetime import date
>>> 
>>> # Create test Fall
>>> fall = Fall.objects.create(
...     zustaendige_beratungsstelle='FBS_1_LE',
...     status='AKTIV'
... )


>>> PersonenbezogeneDaten.objects.create(
...     fall=fall,
...     alias='BERATUNG_TEST_001',
...     rolle_der_ratsuchenden_person='BETROFFENE'
... )


<PersonenbezogeneDaten: Daten für BERATUNG_TEST_001>
>>> print(f"Initial: anzahl={fall.beratungsanzahl}, letzte={fall.letzte_beratung}")
Initial: anzahl=0, letzte=None
>>> Beratung.objects.create(
...     fall=fall,
...     datum=date(2026, 1, 5),
...     durchfuehrungsart='PERSOENLICH',
...     durchfuehrungsort='LEIPZIG_STADT'
... )
<Beratung: Beratung 2026-01-05 für BERATUNG_TEST_001>

## feini

>>> fall.refresh_from_db()
>>> print(f"After Beratung: anzahl={fall.beratungsanzahl}, letzte={fall.letzte_beratung}")

After Beratung: anzahl=1, letzte=2026-01-05

## it gets tracked properly
## deleting for cleanup
>>> fall.delete()
(3, {'core.PersonenbezogeneDaten': 1, 'core.Beratung': 1, 'core.Fall': 1})


>>> print(f"After Beratung: anzahl={fall.beratungsanzahl}, letzte={fall.letzte_beratung}")
After Beratung: anzahl=1, letzte=2026-01-05

## got confused, because why does it still give these info? didnt it delete properly?

>>> fall.delete()
Traceback (most recent call last):
  File "/usr/lib/python3.12/code.py", line 90, in runcode
    exec(code, self.locals)
  File "<console>", line 1, in <module>
  File "/home/violet/repos/WS2025-SE-Bellis-ev/venv/lib/python3.12/site-packages/django/db/models/base.py", line 1172, in delete
    raise ValueError(
ValueError: Fall object can't be deleted because its fall_id attribute is set to None.

### actually no, that shows its gone. the residual data are stored in python, not in the db. yippieee
>>> 

========= GEWALTART ================

(venv) violet@PiltoversFinest:~/repos/WS2025-SE-Bellis-ev/src$ python manage.py dbshell
psql (16.11 (Ubuntu 16.11-0ubuntu0.24.04.1))
SSL connection (protocol: TLSv1.3, cipher: TLS_AES_256_GCM_SHA384, compression: off)
Type "help" for help.

bev_dev=> \dt gewalttat_art
\dt folgen_der_gewalt
\dt fall_folgen_der_gewalt
             List of relations
 Schema |     Name      | Type  |  Owner   
--------+---------------+-------+----------
 public | gewalttat_art | table | bev_user
(1 row)

               List of relations
 Schema |       Name        | Type  |  Owner   
--------+-------------------+-------+----------
 public | folgen_der_gewalt | table | bev_user
(1 row)

                 List of relations
 Schema |          Name          | Type  |  Owner   
--------+------------------------+-------+----------
 public | fall_folgen_der_gewalt | table | bev_user
(1 row)



>>> from core.models import GewalttatArt, FolgenDerGewalt, Fall, PersonenbezogeneDaten, Fall_FolgenDerGewalt
>>> 
>>> # Test GewalttatArt hierarchy
>>> hauptkat = GewalttatArt.objects.create(
...     name="Sexuelle Belästigung",
...     ist_unterkategorie=False
... )
 = GewalttatArt.objects.create(
    name="Sexuelle Belästigung – im öffentlichen Raum",
    ist_unterkategorie=True,
    hauptkategorie=hauptkat
)

unterkat2 = GewalttatArt.objects.create(
    name="Sexuelle Belästigung – am Arbeitsplatz",
    ist_un>>> 
>>> unterkat1 = GewalttatArt.objects.create(
...     name="Sexuelle Belästigung – im öffentlichen Raum",
...     ist_unterkategorie=True,
...     hauptkategorie=hauptkat
... )
terkategorie=True,
    hauptkategorie=hauptkat
)

>>> 
>>> unterkat2 = GewalttatArt.objects.create(
...     name="Sexuelle Belästigung – am Arbeitsplatz",
...     ist_unterkategorie=True,
...     hauptkategorie=hauptkat
... )


>>> print(f"Hauptkategorie: {hauptkat.name}")
Hauptkategorie: Sexuelle Belästigung

>>> print(f"Unterkategorien: {list(hauptkat.unterkategorien.all())}")
Unterkategorien: [<GewalttatArt: Sexuelle Belästigung – am Arbeitsplatz>, <GewalttatArt: Sexuelle Belästigung – im öffentlichen Raum>]
>>> 


>>> 
>>> # Test GewalttatArt hierarchy
>>> hauptkat = GewalttatArt.objects.create(
...     name="Sexuelle Belästigung",
...     ist_unterkategorie=False
... )
 = GewalttatArt.objects.create(
    name="Sexuelle Belästigung – im öffentlichen Raum",
    ist_unterkategorie=True,
    hauptkategorie=hauptkat
)

unterkat2 = GewalttatArt.objects.create(
    name="Sexuelle Belästigung – am Arbeitsplatz",
    ist_un>>> 
>>> unterkat1 = GewalttatArt.objects.create(
...     name="Sexuelle Belästigung – im öffentlichen Raum",
...     ist_unterkategorie=True,
...     hauptkategorie=hauptkat
... )

>>> print(f"Hauptkategorie: {hauptkat.name}")

Hauptkategorie: Sexuelle Belästigung

>>> print(f"Unterkategorien: {list(hauptkat.unterkategorien.all())}")
Unterkategorien: 
[<GewalttatArt: Sexuelle Belästigung – am Arbeitsplatz>,
 <GewalttatArt: Sexuelle Belästigung – im öffentlichen Raum>]


### self-referential foreign keys are working
### reverse relationps working (hauptkat.unterkategorien.all)
### hierarchy structures working

>>> 
>>> 
>>> # Test FolgenDerGewalt
>>> folge1 = FolgenDerGewalt.objects.create(
...     name="Depression",
...     kategorie="PSYCHISCH"
... )
>>> 
>>> folge2 = FolgenDerGewalt.objects.create(
...     name="Angststörung",
...     kategorie="PSYCHISCH"
... )
>>> 
### tested creation, created 2 consequence types


>>> # Test M2M via Fall_FolgenDerGewalt
>>> fall = Fall.objects.create(
...     zustaendige_beratungsstelle='FBS_1_LE',
...     status='AKTIV'
... )
n.objects.create(
    fall=fall,
    alias='FOLGEN_TEST_001',
    rolle_der_ratsuchenden_person='BET>>> 
>>> PersonenbezogeneDaten.objects.create(
...     fall=fall,
...     alias='FOLGEN_TEST_001',
...     rolle_der_ratsuchenden_person='BETROFFENE'
... )
<PersonenbezogeneDaten: Daten für FOLGEN_TEST_001>
>>> 
>>> 
>>> # Link Fall to consequences
>>> Fall_FolgenDerGewalt.objects.create(
...     fall=fall,
...     folge=folge1,
...     weitere_informationen="Seit 6 Monaten in Behandlung"
... )
<Fall_FolgenDerGewalt: FOLGEN_TEST_001 - Depression>
>>> 
>>> Fall_FolgenDerGewalt.objects.create(
...     fall=fall,
...     folge=folge2
... )
<Fall_FolgenDerGewalt: FOLGEN_TEST_001 - Angststörung>
>>> 
>>> 

Folgen für FOLGEN_TEST_001:
  - Depression (PSYCHISCH)
  - Angststörung (PSYCHISCH)
### junction table creates links correctly 
### queries return all consequences of fall, displays alias and consequence name
### wiedere_informationen field was accepted, even if it wasnt queried



>>> 
>>> # Cleanup
>>> fall.delete()
.delete()
FolgenDerGewalt.objects.all().delete()(4, {'core.PersonenbezogeneDaten': 1, 'core.Fall_FolgenDerGewalt': 2, 'core.Fall': 1})
>>> GewalttatArt.objects.all().delete()
(3, {'core.GewalttatArt': 3})
>>> FolgenDerGewalt.objects.all().delete()
(2, {'core.FolgenDerGewalt': 2})

### CASCADE cleanup

>>>     print(f"  - {c.folge.name} ({c.folge.kategorie})")
Traceback (most recent call last):
  File "/usr/lib/python3.12/code.py", line 63, in runsource
    code = self.compile(source, filename, symbol)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/codeop.py", line 161, in __call__
    return _maybe_compile(self.compiler, source, filename, symbol)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/codeop.py", line 73, in _maybe_compile
    return compiler(source, filename, symbol, incomplete_input=False)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/codeop.py", line 126, in __call__
    codeob = compile(source, filename, symbol, flags, True)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<console>", line 1
    print(f"  - {c.folge.name} ({c.folge.kategorie})")
IndentationError: unexpected indent

### error after cleanup