```markdown

## Step 2: UML to Django Mapping Explanation
============================================================================
## MAPPING OUR MVP UML TO DJANGO
## What Django Gives You vs. What You Need to Write
============================================================================

Let's go through our UML diagram entity by entity and see what Django handles
automatically versus what we need to code ourselves.

## ✅ DJANGO GIVES YOU FOR FREE

### 1. User, Session, Role, PermissionSet → Django Auth System

**What our UML says:**
- User entity with username, email, password_hash
- Session entity for login tracking
- Role entity with BASIS/ERWEITERT/ADMINISTRATOR
- PermissionSet with permission flags

**What Django provides:**
Django has a built-in `User` model and authentication system! You don't build
this from scratch.

**File: users/models.py**
from django.contrib.auth.models import AbstractUser, Group
Extend Django's User instead of creating from scratch

class User(AbstractUser):
# Django already has: username, email, password (auto-hashed!),
# is_active, date_joined
# We just add our custom field:
role = models.ForeignKey('Role', on_delete=models.PROTECT)


# Django's login() and logout() are built-in!


**File: users/models.py (continued)**

class Role(models.Model):
ROLE_CHOICES = [
('BASIS', 'Basis'),
('ERWEITERT', 'Erweitert'),
('ADMINISTRATOR', 'Administrator'),
]
name = models.CharField(max_length=20, choices=ROLE_CHOICES, unique=True)
description = models.TextField()

======================================================================
# This replaces our PermissionSet entity -> Django has a better way:
# -> We Use Django's built-in permission system
class Meta:
    permissions = [
        ('view_cases', 'Can view cases'),
        ('edit_cases', 'Can edit cases'),
        ('delete_cases', 'Can delete cases'),
        ('manage_reference_data', 'Can manage reference data'),
        ('manage_users', 'Can manage users'),
    ]


## Why?
- Password hashing automatic
- Session management built-in (no need for Session entity stuff!)
- `user.has_perm('cases.edit_cases')` -> checks permissions
- Admin interface for user management FREE

## What we write instead:
- Create 3 Role records in a data migration (BASIS, ERWEITERT, ADMINISTRATOR)
- Assign permissions to each role
- Middleware to check `user.role.has_perm()` before views run

## Files involved:
- `users/models.py` - User and Role models
- `users/migrations/0002_seed_roles.py` - Data migration to create 3 roles
- `users/middleware.py` - Permission checking middleware

---

### 2. Database Relationships → Django ORM

**What our UML says:**
- Fall 1-to-1 PersonenbezogeneDaten
- Fall 1-to-many Beratung
- Gewalttat many-to-many GewalttatArt (via junction table)

**What Django provides:**
Django ORM creates all foreign keys, junction tables, and cascade deletes
automatically!

**Example - One to One:**

class Fall(models.Model):
fall_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
# ... other fields ...

class PersonenbezogeneDaten(models.Model):
fall = models.OneToOneField(Fall, on_delete=models.CASCADE,
related_name='personenbezogene_daten')
# Django creates the FK and enforces one-to-one automatically!

text

Now you can do: `fall.personenbezogene_daten.alter` (accesses related data)

**Example - One to Many:**

class Beratung(models.Model):
fall = models.ForeignKey(Fall, on_delete=models.CASCADE,
related_name='beratungen')
datum = models.DateField()

text

Now you can do: `fall.beratungen.all()` (gets all Beratung for this Fall)

**Example - Many to Many:**

class Gewalttat(models.Model):
gewalttat_arten = models.ManyToManyField('GewalttatArt',
through='Gewalttat_GewalttatArt')
# Django creates the junction table automatically!

class Gewalttat_GewalttatArt(models.Model):
gewalttat = models.ForeignKey(Gewalttat, on_delete=models.CASCADE)
art = models.ForeignKey(GewalttatArt, on_delete=models.RESTRICT)
andere_details = models.TextField(blank=True)

text

Now you can do: `gewalttat.gewalttat_arten.add(art_object)`

**What you write:**
- Just the model definitions (like above)
- Run `makemigrations` and `migrate`

**Django handles:**
- Creating all tables
- Creating indexes on foreign keys
- Enforcing CASCADE/RESTRICT/SET_NULL
- Query optimization

---

### 3. Forms & Validation → Django Forms

**What our UML says:**
- ValidationService with validateInput(), validatePassword(), etc.
- ValidationResult with error messages

**What Django provides:**
Django has a complete form system with built-in validation!

**File: cases/forms.py**

from django import forms
from .models import Fall, PersonenbezogeneDaten

class FallForm(forms.ModelForm):
class Meta:
model = Fall
fields = ['alias', 'zustaendige_beratungsstelle', 'informationsquelle']

text
# Django automatically validates:
# - Required fields
# - Unique constraint on alias
# - Enum choices (only valid beratungsstelle values)

# You add custom validation:
def clean_alias(self):
    alias = self.cleaned_data['alias']
    if len(alias) < 3:
        raise forms.ValidationError("Alias muss mindestens 3 Zeichen haben")
    return alias

text

**In your view:**

def create_fall(request):
if request.method == 'POST':
form = FallForm(request.POST)
if form.is_valid(): # Runs all validations!
fall = form.save() # Saves to database
return redirect('fall_detail', pk=fall.fall_id)
else:
# form.errors contains all validation errors
return render(request, 'fall_form.html', {'form': form})

text

**What you write:**
- Form classes in `forms.py`
- Custom `clean_*` methods for special validation rules
- Template to display the form

**Django handles:**
- Type validation (DateField only accepts dates, etc.)
- Required field checking
- Unique constraint checking
- HTML form rendering
- Error message display

**Our ValidationService becomes:**
Small utility functions for complex validations that Django doesn't cover.

**File: cases/services.py**

class ValidationService:
@staticmethod
def validate_taeterinnen_json(json_str):
# Custom validation for JSON structure
try:
data = json.loads(json_str)
if not isinstance(data, list):
return False, "Must be array"
for item in data:
if 'geschlecht' not in item or 'verhaeltnis' not in item:
return False, "Missing required fields"
return True, None
except json.JSONDecodeError:
return False, "Invalid JSON"

text

---

### 4. Admin Interface → Django Admin

**What our UML says:**
- ADMINISTRATOR role can create/manage users

**What Django provides:**
FREE admin interface at `/admin` for all your models!

**File: cases/admin.py**

from django.contrib import admin
from .models import Fall, Beratung, Gewalttat

@admin.register(Fall)
class FallAdmin(admin.ModelAdmin):
list_display = ['alias', 'status', 'erstellungsdatum', 'bearbeitet_von']
list_filter = ['status', 'zustaendige_beratungsstelle']
search_fields = ['alias']
readonly_fields = ['erstellungsdatum', 'letzte_bearbeitung']

text

Now at `http://localhost:8000/admin/` you have a full UI to view/edit/delete
Fall records. No HTML/CSS/JavaScript needed!

**What you write:**
- Admin class configurations (what fields to show, filters, etc.)

**Django handles:**
- Entire UI
- CRUD operations
- Permission checking (only staff/superuser access)
- Change history logging

---

## ⚠️ YOU NEED TO WRITE (NO DJANGO MAGIC)

### 1. FallManager Business Logic

**What our UML says:**
- FallManager.createFall() creates Fall + PersonenbezogeneDaten atomically
- FallManager.addBeratung() increments Fall.beratungsanzahl

**Django doesn't have:**
A "Manager" concept like our UML. You write this yourself.

**File: cases/managers.py**

from django.db import transaction
from .models import Fall, PersonenbezogeneDaten, Beratung

class FallManager:
@staticmethod
@transaction.atomic # Django decorator for database transactions
def createFall(fall_data, person_data):
"""
Creates Fall and PersonenbezogeneDaten together.
If either fails, both roll back.
"""
fall = Fall.objects.create(**fall_data)
person_data['fall'] = fall
PersonenbezogeneDaten.objects.create(**person_data)
return fall

text
@staticmethod
def addBeratung(fall_id, beratung_data):
    """
    Creates Beratung and updates Fall aggregate fields.
    """
    fall = Fall.objects.get(fall_id=fall_id)
    beratung_data['fall'] = fall
    beratung = Beratung.objects.create(**beratung_data)
    
    # Update aggregates
    fall.beratungsanzahl = fall.beratungen.count()
    fall.letzte_beratung = beratung.datum
    fall.save()
    
    return beratung

text

**Why not in the Model itself?**
Could be! Some teams put this logic in custom model managers. Either works.

---

### 2. Search Functionality

**What our UML says:**
- Fall.searchByAlias()
- Fall.searchByDateRange()

**Django provides:**
QuerySet API for database queries, but you write the search logic.

**File: cases/views.py**

from django.db.models import Q

def search_cases(request):
query = request.GET.get('q', '')
date_from = request.GET.get('date_from')
date_to = request.GET.get('date_to')

text
cases = Fall.objects.all()

if query:
    # Search alias (case-insensitive, partial match)
    cases = cases.filter(alias__icontains=query)

if date_from and date_to:
    cases = cases.filter(erstellungsdatum__range=[date_from, date_to])

return render(request, 'search_results.html', {'cases': cases})

text

**Django gives you:**
- `filter()`, `exclude()`, `order_by()` query methods
- `__icontains`, `__range`, `__gte` lookup operators
- Automatic SQL generation (you never write SELECT statements)

**You write:**
- View logic to combine filters based on user input

---

### 3. JSON Field Handling (taeterinnen_details)

**What our UML says:**
- Gewalttat.taeterinnen_details is JSON
- addTaeterIn() method appends to it

**Django provides:**
JSONField type (since Django 3.1)!

**File: cases/models.py**

class Gewalttat(models.Model):
taeterinnen_details = models.JSONField(default=list)

text
def add_taeterin(self, geschlecht, verhaeltnis):
    """Custom method to append to JSON array"""
    self.taeterinnen_details.append({
        'geschlecht': geschlecht,
        'verhaeltnis': verhaeltnis
    })
    self.save()

text

**Django handles:**
- Storing/retrieving JSON in PostgreSQL
- Validation that it's valid JSON

**You write:**
- Methods to manipulate the JSON structure
- Queries like: `Gewalttat.objects.filter(taeterinnen_details__contains={'geschlecht': 'männlich'})`

---

### 4. Enum Choices

**What our UML says:**
- Lots of enum fields (status, durchfuehrungsart, etc.)

**Django provides:**
Choices system!

**File: cases/models.py**

class Fall(models.Model):
class Status(models.TextChoices):
AKTIV = 'AKTIV', 'Aktiv'
ARCHIVIERT = 'ARCHIVIERT', 'Archiviert'

text
status = models.CharField(max_length=20, choices=Status.choices, 
                           default=Status.AKTIV)

text

**Django handles:**
- Dropdown in forms automatically
- Validation (only AKTIV or ARCHIVIERT allowed)
- Display value (shows "Aktiv" in templates, stores "AKTIV" in DB)

**You write:**
- The choices definition

---

## 📁 WHERE THINGS GO IN DJANGO

cases/ # One Django "app" per logical grouping
├── models.py # All entity classes (Fall, Beratung, etc.)
├── managers.py # FallManager business logic
├── services.py # ValidationService utilities
├── views.py # HTTP request handlers
├── forms.py # Form definitions
├── urls.py # URL routing for this app
├── admin.py # Admin interface config
├── tests.py # Unit tests
├── migrations/ # Database schema versions
│ ├── 0001_initial.py # First migration (creates tables)
│ ├── 0002_add_gewalttat.py # Added Gewalttat model
│ └── 0003_seed_reference.py # Data migration (seeds GewalttatArt)
└── templates/cases/ # HTML templates
├── fall_list.html
├── fall_form.html
└── fall_detail.html

text

**models.py** = Your UML entities (Fall, Beratung, Gewalttat)
**managers.py** = Your UML managers (FallManager)
**services.py** = Your UML services (ValidationService)
**views.py** = Controller logic (not in UML - web layer)
**forms.py** = Form validation (not in UML - web layer)
**migrations/** = Database schema (generated by Django)

---

## 🗄️ DATABASE

You DON'T directly create a database schema. Django does it.

**Process:**
1. Write models in `models.py`
2. Run `python manage.py makemigrations` → Django creates migration file
3. Run `python manage.py migrate` → Django applies to PostgreSQL

**Where is the database?**
Configured in `settings.py`:

DATABASES = {
'default': {
'ENGINE': 'django.db.backends.postgresql',
'NAME': 'bev_mvp',
'USER': 'postgres',
'PASSWORD': 'your_password',
'HOST': 'localhost',
'PORT': '5432',
}
}

text

**You never write:**
- CREATE TABLE statements
- ALTER TABLE statements
- Foreign key constraints

**Django generates all SQL automatically from your models!**

---

## SUMMARY TABLE

| UML Component | Django Equivalent | Auto or Manual? |
|---------------|-------------------|-----------------|
| User entity | AbstractUser | 90% auto, extend it |
| Session entity | Built-in sessions | 100% auto |
| Role/PermissionSet | Groups + Permissions | 80% auto, configure it |
| Fall, Beratung models | Model classes | Manual class definition, auto DB creation |
| Foreign keys | ForeignKey fields | Auto relationship handling |
| Cascade delete | on_delete parameter | Auto enforcement |
| ValidationService | Form validation | Mix (basic auto, complex manual) |
| FallManager | Custom manager class | 100% manual |
| Search methods | QuerySet methods | Manual logic, auto SQL |
| JSON fields | JSONField | Auto storage, manual manipulation |
| Enums | TextChoices | Manual definition, auto validation |
| Admin UI | django.contrib.admin | 95% auto, customize as needed |

The pattern: Django handles database/auth/forms plumbing. You write business logic.