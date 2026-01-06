### Here i want to document some of the stuff we used to mplement this system 
### So i'll actually remember what i did

### >>>> Self-Referential foreign keys <<<< 

hauptkategorie = models.ForeignKey(
    'self',             # Referencing / pointing back at the same model
    on_delete=models.SET_NULL,
    null=True,          # Top-level categories have NULL
    blank=True,
    related_name='unterkategorien'
)

### basically its a hierarchical tree made up of the same model.
### Instead of creating seperate tables for Category and SubCategory, we use 1 table, and let it reference itself.
### like theres a (sub)category of violence that has a parent catory. That is also a category of violence. And so on.
### Every category can have a parent and child category. Toplevel doesnt have any parents (RIP)

USage example:

# Top-level category
kategorie = GewalttatArt.objects.create(
    name="Sexuelle Belästigung",
    ist_unterkategorie=False, 
    hauptkategorie=None  # No parent
)

# Subcategory
subkategorie = GewalttatArt.objects.create(
    name="Sexuelle Belästigung – im öffentlichen Raum",
    ist_unterkategorie=True,
    hauptkategorie=kategorie  # Parent category
)

# Access hierarchy
kategorie.unterkategorien.all()  # Returns subcategories

### >>>> junction tables <<<< 

### So we had hierarchies with one model. now we have two differet models, with many to many relationships
### like there are a lot of students and a lot of courses, a student can take many courses, a course has many students
### to link the two, we have a seperate junction table in the middle. StudentCourse
### now django has integrated Many2Many solutions buuut apparently they dont support extra fields (weitere informationen etc)
### plus it gives us extra control for stuff like CASCADE delete.

unique_together constraint:

unique_together = [['gewalttat', 'art']]

### prevents the same violence type being selected multiple times for one incident. Should still work if theres multiple incidents in one case.
### works on database level, not through django


### >>>> forward references  / stringforeignkeys <<<< 
gewalttat = models.ForeignKey(
    'Gewalttat',  # String - model not yet defined
    on_delete=models.CASCADE
)

### needed as we implement and build the app because sometimes stuff doesnt exist yet. 
### this allowed junction tables to be created before everything else is in place
### django later resolves the string reference after all the models are loaded.


### >>>> JSONField for perpetrator details <<<< 

### Sometimes you need to store related items but dont need a full table
### JSONField lets you store an array of objects directly in the database
### keeps models simpler
### should also be used for simple data only

Structure:

taeterinnen_details = models.JSONField(default=list, blank=True)


Used in / The expected .JSON output:
[
    {
        "geschlecht": "männlich",
        "verhaeltnis_zur_ratsuchenden_person": "Partner:in"
    },
    {
        "geschlecht": "weiblich",
        "verhaeltnis_zur_ratsuchenden_person": "Bekannte:r"
    }
]



### >>>> conditional field patterns <<<< 

### Basically some fields should only be filled based on the value of others

Conditional Fields Pattern


If zahl_der_vorfaelle = 'GENAUE_ZAHL' → zahl_der_vorfaelle_genau should be filled
If anzahl_taeterinnen = 'GENAUE_ZAHL' → anzahl_taeterinnen_genau should be filled
If alter_tat_keine_angabe = True → alter_zum_zeitpunkt_der_tat should be NULL
If zeitraum_keine_angabe = True → zeitraum_von and zeitraum_bis should be NULL
​
### Its enforced in Django, with form validation, database doesnt really get the concept