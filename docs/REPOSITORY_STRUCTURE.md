# Repository Structure & System Overview

This document provides a complete visual representation of the WS2025-SE-Bellis-ev repository structure, system architecture, and comprehensive testing overview.

---

## Quick System Overview

**B-EV** (Beratung und Empowerment für Überlebende von Gewalt) is a Django-based case management system for documenting and tracking sexual violence counseling services. The system implements a three-tier permission model (BASIS, ERWEITERT, ADMIN) with comprehensive CRUD operations for case management, consultation tracking, and violence incident documentation.

### Key Features:
- **Case Management**: Track individual cases (Fall) with associated personal data
- **Permission System**: Role-based access control with granular permissions
- **Consultation Tracking**: Record individual counseling sessions (Beratung)
- **Violence Documentation**: Track violence incidents (Gewalttat) with detailed metadata
- **Data Privacy**: Separate demographic data (PersonenbezogeneDaten) from case records
- **Reference Data**: Hierarchical violence categories (GewalttatArt) and user role definitions

---

## System Architecture

### Three-Tier Permission Model

```
BASIS (Counselor)
  ├─ Can read cases
  ├─ Can create cases
  ├─ Can edit own cases
  ├─ Can soft-delete (archive) own cases
  └─ Cannot hard-delete

ERWEITERT (Senior Counselor)
  ├─ All BASIS permissions +
  ├─ Can soft-delete any case
  ├─ Can manage multiple cases
  └─ Cannot hard-delete

ADMIN (System Administrator)
  ├─ All permissions
  ├─ Can hard-delete cases (permanent + CASCADE)
  ├─ Can manage users
  └─ Can view system metrics
```

### Data Flow Architecture

```
User Request
    ↓
[Django Views] - Request handling & template rendering
    ↓
[Forms] - Input validation & form generation
    ↓
[Services] - Business logic & data processing
    ├─ FallManager - Case lifecycle management
    ├─ ValidationService - Data validation rules
    └─ Session Manager - Consultation tracking
    ↓
[Models] - Database representation
    ├─ Fall (main case entity)
    ├─ PersonenbezogeneDaten (demographic data)
    ├─ Beratung (consultation sessions)
    ├─ Gewalttat (violence incidents)
    └─ GewalttatArt (reference data - violence categories)
    ↓
[PostgreSQL Database] - Persistent storage
```

### Key Model Relationships

```
Fall (1) ────── (1) PersonenbezogeneDaten
  │
  ├── (1:N) Beratung (consultations)
  │
  ├── (1:N) Gewalttat (violence incidents)
  │   │
  │   └── (N:M) GewalttatArt (via Gewalttat_GewalttatArt junction)
  │
  └── (FK) User (bearbeitet_von - who last edited)

PersonenbezogeneDaten
  ├─ CASCADE delete with Fall
  └─ Contains all sensitive demographic data

GewalttatArt (Self-referential hierarchy)
  ├─ hauptkategorie (FK to 'self')
  └─ Can form category hierarchies (parent → child)
```

---

## Full Directory Tree

```
WS2025-SE-Bellis-ev/
├── .editorconfig                    # Editor configuration file
├── .dockerignore                    # Docker ignore patterns
├── .git/                            # Git repository metadata
├── .gitattributes                   # Git attributes configuration
├── .gitignore                       # Git ignore patterns
├── .gitmodules                      # Git submodules configuration
├── .github/                         # GitHub-specific configuration
│   ├── CODE_OF_CONDUCT.md
│   ├── CONTRIBUTING.md
│   ├── SECURITY.md
│   ├── SUPPORT.md
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   ├── feature_request.md
│   │   ├── question.md
│   │   └── README.md
│   └── PULL_REQUEST_TEMPLATE/
│       ├── PULL_REQUEST_TEMPLATE.md
│       └── README.md
├── LICENSE                          # Project license file
├── README.md                        # Main project README
├── VERSIONING.md                    # Versioning guidelines
├── requirements.txt                 # Python dependencies
├── UML-1.pdf                        # UML diagram PDF
├── Requirement Engineering mit Notizen.pdf
│
├── docs/                            # Documentation directory
│   ├── README.md                    # Documentation home
│   ├── STYLEGUIDE.md                # Documentation style guide
│   ├── REPOSITORY_STRUCTURE.md      # THIS FILE
│   │
│   ├── architecture/                # Architecture documentation
│   │   ├── MVP_Definition.md
│   │   ├── READ_THIS_PLEASE_THANKS.md
│   │   │
│   │   ├── FULL_UML/                # Full system UML diagrams
│   │   │   ├── FULL_UML_Clean/
│   │   │   ├── FULL_UML_Groups/
│   │   │   └── FULL_UML_Visuals/
│   │   │       ├── Full_UML_Class_Diagram.png
│   │   │       └── Full_UML_Component_Diagram.png
│   │   │
│   │   ├── MVP_UML/                 # MVP-specific UML diagrams
│   │   │   ├── MVP_UML_Clean/
│   │   │   ├── MVP_UML_Groups/
│   │   │   │   ├── 01_User&Permission_System/
│   │   │   │   ├── 02_Case_Management/
│   │   │   │   ├── 03_Reference_Data/
│   │   │   │   ├── 04_Validation_System/
│   │   │   │   ├── 05_Manager_Classes/
│   │   │   │   ├── 06_Infrastructure/
│   │   │   │   └── 07_Relationships/
│   │   │   └── MVP_UML_Visuals/
│   │   │       ├── MVP_UML_Class_Diagram.png
│   │   │       └── MVP_UML_Component_Diagram.png
│   │   │
│   │   ├── MVP_DJANGO/              # Django-specific implementation
│   │   │   ├── DIAGRAM_CLEAN_UPDATED_WITH_DJANGO.md
│   │   │   ├── VIsuals/
│   │   │   │
│   │   │   ├── Cheatsheets_And_Guides/
│   │   │   │   ├── Quick_Reference_commands.md
│   │   │   │   ├── What_to_Do.md
│   │   │   │   └── Too_Long_didnt_read/
│   │   │   │       ├── 01_Django_Basics_TLDR.md
│   │   │   │       ├── 02_GitHub_Basics_TLDR.md
│   │   │   │       ├── 03_Postgres_Setup_TLDR.md
│   │   │   │       ├── 04_Django_Settings_Postgres_TLDR.md
│   │   │   │       ├── 05_.env_Files.md
│   │   │   │       └── 06_Verification_and_Migration.md
│   │   │   │
│   │   │   └── Mapping_this_shit/
│   │   │       ├── Implementation_Priority.md
│   │   │       ├── Model_to_File_Mapping.md
│   │   │       └── Repo_structure_with_MVP_Mapping.md
│   │   │
│   │   └── Outdated_Shit_I_Keep_Here_for_Reference/
│   │       ├── Django_GitHub_Basics_Mainly_generated_By_Claude/
│   │       ├── Django-Database_Mapping-fun.md
│   │       └── Mapping.md
│   │
│   ├── team_documentation/          # Team-specific documentation
│   │   └── Violet/
│   │       ├── AI_Usage_Principles.md
│   │       ├── GitHub_Commit_and_Push.md
│   │       └── MasterPrompt_3.md
│   │
│   └── user_documenation/           # User-facing documentation
│       └── (content directory)
│
├── src/                             # Source code directory
│   ├── manage.py                    # Django management script
│   ├── README.md                    # Source code documentation
│   │
│   ├── B_EV/                        # Main Django project package
│   │   ├── __init__.py
│   │   ├── __pycache__/
│   │   │   ├── __init__.cpython-312.pyc
│   │   │   └── settings.cpython-312.pyc
│   │   ├── asgi.py                  # ASGI configuration
│   │   ├── settings.py              # Django settings
│   │   ├── urls.py                  # URL routing
│   │   └── wsgi.py                  # WSGI configuration
│   │
│   └── core/                        # Core application module
│       ├── __init__.py
│       ├── admin.py                 # Django admin configuration
│       ├── apps.py                  # App configuration
│       ├── decorators.py            # Custom permission decorators
│       ├── forms.py                 # Legacy form imports (redirects to forms/)
│       ├── models.py                # Legacy models.py (redirects to models/)
│       ├── views.py                 # Legacy views.py (redirects to views/)
│       ├── tests.py                 # Unit tests
│       ├── urls.py                  # URL routing configuration
│       ├── fixtures/                # JSON fixtures for test data
│       │   └── (seed data for testing)
│       │
│       ├── forms/                   # Django forms package
│       │   ├── __init__.py
│       │   ├── fall_forms.py         # Case/incident-related forms
│       │   └── user_forms.py         # User management forms
│       │
│       ├── managers/                # Custom managers and business logic
│       │   ├── __init__.py
│       │   ├── fall_manager.py       # Case (Fall) lifecycle management
│       │   └── session_manager.py    # Consultation session management
│       │
│       ├── models/                  # Modular models package
│       │   ├── __init__.py
│       │   ├── fall_models.py        # Fall, PersonenbezogeneDaten, Beratung, Gewalttat
│       │   ├── user_models.py        # User, Role, PermissionSet models
│       │   └── reference_models.py   # GewalttatArt, Jurisdiction models
│       │
│       ├── services/                # Business logic services
│       │   ├── __init__.py
│       │   ├── validation_service.py # Core data validation logic
│       │   └── (additional services)
│       │
│       ├── validators/              # Custom validators
│       │   ├── __init__.py
│       │   └── (field validation rules)
│       │
│       ├── views/                   # Views organized by feature
│       │   ├── __init__.py
│       │   ├── case_views.py         # Case CRUD operations
│       │   ├── beratung_views.py     # Consultation management
│       │   ├── gewalttat_views.py    # Violence incident tracking
│       │   └── permission_views.py   # Permission-protected views
│       │
│       ├── templates/               # HTML templates
│       │   └── core/                # Templates for core app
│       │       ├── case_list.html
│       │       ├── case_detail.html
│       │       ├── case_create.html
│       │       └── (additional templates)
│       │
│       └── migrations/              # Database migrations
│           └── __init__.py
│
├── test_views_comprehensive.py      # Phase 3B comprehensive test suite
├── test_views_manual.py             # Manual testing utilities
│
└── test/                            # Testing directory
    └── README.md                    # Testing documentation
```

## Directory Summary

| Directory | Purpose |
|-----------|---------|
| `.github/` | GitHub-specific configuration (issues, PRs, templates) |
| `docs/` | Complete project documentation |
| `docs/architecture/` | System architecture and design documents |
| `docs/architecture/FULL_UML/` | Full system UML diagrams and visualizations |
| `docs/architecture/MVP_UML/` | MVP-phase UML diagrams and visualizations |
| `docs/architecture/MVP_DJANGO/` | Django implementation specifics |
| `docs/team_documentation/` | Team-specific guides and documentation |
| `src/` | Python source code (Django project) |
| `src/B_EV/` | Main Django project configuration |
| `src/core/` | Core Django application (Phase 1 MVP implementation) |
| `src/core/models/` | Modular models package (Fall, PersonenbezogeneDaten, Beratung, Gewalttat) |
| `src/core/forms/` | Django forms for Fall and User interactions |
| `src/core/managers/` | Custom managers for complex business logic |
| `src/core/services/` | Business logic services (validation, etc.) |
| `src/core/fixtures/` | Test data fixtures (JSON files) |
| `src/core/templates/` | HTML templates for core app |
| `test/` | Testing resources and documentation |

## Key Files

| File | Description |
|------|-------------|
| `README.md` | Main project introduction and overview |
| `VERSIONING.md` | Project versioning guidelines |
| `requirements.txt` | Python package dependencies |
| `LICENSE` | Project license terms |
| `.env` | Environment variables (database, Django settings) |
| `.coderabbit.yaml` | CodeRabbit configuration for code reviews |

## Phase 1 Implementation Status

**Core Models Implemented:**
- `Fall` - Main case entity with metadata and aggregate counters
- `PersonenbezogeneDaten` - 1:1 personal demographic data (privacy by design)
- `Beratung` - Individual consultation sessions (linked to Fall)
- `Gewalttat` - Violence incident records with multiple fields

**Database:**
- PostgreSQL configured and running
- Database `bev_dev` and user `bev_user` created
- Django settings configured with environment variables (.env)

**Project Structure:**
- Modular models package under `src/core/models/`
- Separate packages for forms, managers, and services
- Fixtures and templates directories ready for content
- Database migrations initialized

---

## Phase 3B Implementation - Views & Testing

### Views Implemented

**Case Management Views:**
- `CaseListView` - List all cases with permission filtering
- `CaseDetailView` - View complete case with all consultations and incidents
- `CaseCreateView` - Create new case with demographic data
- `CaseEditView` - Edit case information
- `CaseDeleteView` - Soft delete (archive) or hard delete (permanent)
- `CaseCloseView` - Mark case as completed

**Consultation Views:**
- `BeratungAddView` - Add consultation session to case
- `BeratungListView` - List consultations for a case
- `BeratungEditView` - Edit consultation details

**Violence Incident Views:**
- `GewaltatAddView` - Add violence incident to case
- `GewaltatListView` - List incidents for a case
- `GewaltatDetailView` - View incident details

### Permission Decorators

```python
@permission_required('can_edit_cases')
def case_edit(request, fall_id):
    # Only users with can_edit_cases permission
    
@permission_required('can_delete_cases')
def case_soft_delete(request, fall_id):
    # Soft delete (archive) - ERWEITERT+
    
@permission_required('can_hard_delete_cases')
def case_hard_delete(request, fall_id):
    # Hard delete (permanent) - ADMIN only
```

---

## Comprehensive Test Suite (Phase 3B)

### Test File: `test_views_comprehensive.py`

**Purpose:** Verify all Phase 3B features including CRUD operations, permission boundaries, form validation, and database cascading.

**Test Coverage (12 comprehensive tests):**

| Test # | Name | Purpose | Validates |
|--------|------|---------|-----------|
| 1 | Authentication Required | Verify unauthenticated users redirected | 302 redirect to login |
| 2 | Case List View (BASIS) | Verify case list renders for authenticated user | 200 response, case count |
| 3 | Case Detail View | Verify case details with consultations | 200 response, related data |
| 4 | Case Creation (Complete) | Verify full form submission with all fields | 302 redirect + DB creation |
| 5 | Add Beratung Session | Verify consultation creation & aggregates | Beratung count + Fall update |
| 6 | Add Gewalttat Incident | Verify violence incident with M2M relations | Incident count + M2M links |
| 7 | BASIS Can't Delete | Verify BASIS users cannot delete cases | 403 Forbidden response |
| 8 | ERWEITERT Soft Delete | Verify ERWEITERT can archive cases | 302 redirect + status=ARCHIVIERT |
| 9 | ERWEITERT Can't Hard Delete | Verify ERWEITERT cannot permanently delete | 403 Forbidden response |
| 10 | ADMIN Hard Delete | Verify ADMIN can permanently delete + CASCADE | 302 redirect + DB deletion |
| 11 | Case Edit Operation | Verify case field updates | 302 redirect + DB update |
| 12 | Close Case | Verify case completion with date stamp | 302 redirect + timestamps |

### Test Architecture

```
Test Setup Phase:
├─ Load test users (BASIS, ERWEITERT, ADMIN)
├─ Verify role permissions
├─ Load reference data (GewalttatArt)
└─ Create initial test case

Test Execution (12 Tests):
├─ Authentication & Authorization
├─ CRUD Operations
│  ├─ Create (complete form validation)
│  ├─ Read (detail views)
│  ├─ Update (field modifications)
│  └─ Delete (soft & hard)
├─ Relationship Management
│  ├─ Beratung ↔ Fall aggregates
│  ├─ Gewalttat ↔ GewalttatArt (M2M)
│  └─ CASCADE deletion verification
├─ Permission Boundaries
│  ├─ BASIS limitations
│  ├─ ERWEITERT scope
│  └─ ADMIN full access
└─ Form Validation & Database Integrity

Verification Methods:
├─ HTTP status codes (200, 302, 403)
├─ Database record creation/deletion
├─ Aggregate field updates
├─ Cascade behavior verification
└─ Template rendering
```

### Test Data Fixtures

The test suite uses Django fixtures to load:

```json
{
  "users": [
    {"username": "user_basis", "role": "BASIS"},
    {"username": "user_erweitert", "role": "ERWEITERT"},
    {"username": "user_admin", "role": "ADMIN"}
  ],
  "reference_data": [
    "GewalttatArt (violence categories with hierarchy)",
    "Jurisdiction data",
    "Beratungsstelle locations"
  ]
}
```

### Running the Tests

```bash
# Run comprehensive test suite
python manage.py shell < test_views_comprehensive.py

# Expected output:
# ✓ Authentication checks
# ✓ CRUD operations
# ✓ Permission boundaries
# ✓ Form validation
# ✓ Database integrity
# Phase 3B implementation verified.
```

### Test Results Summary

The comprehensive test suite validates:
- ✓ **Authentication**: Unauthenticated users redirected to login
- ✓ **Authorization**: Permission system enforced correctly
- ✓ **CRUD Operations**: Full create, read, update, delete functionality
- ✓ **Data Integrity**: Aggregate counters updated automatically
- ✓ **Relationships**: M2M and FK relationships working correctly
- ✓ **CASCADE Behavior**: Related records deleted with parent
- ✓ **Form Validation**: Complete form submissions processed correctly
- ✓ **Status Workflows**: Case lifecycle (created → updated → closed/archived)

---
| `docs/STYLEGUIDE.md` | Documentation style guidelines |
| `docs/architecture/MVP_Definition.md` | MVP scope and definitions |
| `src/manage.py` | Django project management interface |
| `src/B_EV/settings.py` | Django project settings and configuration |
| `src/test_views_comprehensive.py` | Phase 3B comprehensive test suite |
| `src/test_views_manual.py` | Manual testing utilities |

---

## How the System Works

### 1. Case Creation Flow

```
User clicks "Create Case"
    ↓
CaseCreateView loads form template
    ↓
User fills out:
  - Case data (Beratungsstelle, info source, etc.)
  - Personal data (alias, age, gender, etc.)
    ↓
Form validation:
  - Check required fields
  - Validate choices
  - Verify aliases are unique
    ↓
FallManager.createFall(fall_data, personen_data)
    ├─ Creates Fall instance
    ├─ Creates PersonenbezogeneDaten (1:1)
    ├─ Sets bearbeitet_von to current user
    └─ Saves both to database
    ↓
Database results:
  - New Fall with UUID
  - Linked PersonenbezogeneDaten
  - Ready for consultations/incidents
    ↓
Redirect to case detail view
```

### 2. Consultation Tracking Flow

```
User views case detail page
    ↓
User clicks "Add Consultation"
    ↓
BeratungAddView renders form
    ↓
User fills:
  - Date
  - Method (phone, in-person, video, etc.)
  - Location
  - Notes
    ↓
Form validates & saves Beratung
    ↓
Post-save signal:
  - Fall.beratungsanzahl += 1
  - Fall.letzte_beratung = this session date
  - Fall.letzte_bearbeitung updated
    ↓
Case detail page shows:
  - Total consultation count
  - Last consultation date
  - Complete session list
```

### 3. Violence Incident Documentation

```
User views case detail
    ↓
User clicks "Add Incident"
    ↓
GewaltatAddView renders form with:
  - Age at time of incident
  - Date range
  - Number of incidents
  - Number of perpetrators
  - Perpetrator details (JSON)
  - Violence type(s) via M2M
  - Location
  - Legal action status
  - Medical/evidence response
    ↓
Form validation:
  - Check conditional fields
    - If "exact number" selected → genau field required
    - If "no info" checked → date fields can be null
  - Validate date ranges
  - Validate M2M violence types
    ↓
Gewalttat_GewalttatArt junction created:
  - Link incident to violence categories
  - Support multiple violence types per incident
  - Unique constraint prevents duplicates
    ↓
Case detail shows:
  - All incidents with details
  - Linked violence categories
  - Sorted by date (most recent first)
```

### 4. Permission System

```
Request comes in
    ↓
@permission_required decorator checks:
  ├─ User authenticated?
  ├─ User role exists?
  └─ Role has required permission?
    ↓
Check PermissionSet for role:
  ├─ can_edit_cases (BASIS+)
  ├─ can_delete_cases (ERWEITERT+) → soft delete only
  ├─ can_hard_delete_cases (ADMIN only) → permanent
  └─ (other permissions)
    ↓
Permission granted?
  ├─ Yes → Proceed with view
  └─ No → Return 403 Forbidden
    ↓
Operation completes with audit trail:
  - bearbeitet_von recorded
  - letzte_bearbeitung timestamped
  - All changes logged
```

### 5. Soft vs. Hard Delete

```
Soft Delete (Archive):
  ├─ User: ERWEITERT or ADMIN
  ├─ Action: Mark Fall.status = 'ARCHIVIERT'
  ├─ Data: Remains in database
  ├─ Recovery: Case can be unarchived
  └─ Use case: Temporary closure, seasonal archives

Hard Delete (Permanent):
  ├─ User: ADMIN only
  ├─ Action: Django .delete()
  ├─ Data: Completely removed
  ├─ CASCADE behavior:
  │  ├─ PersonenbezogeneDaten deleted (1:1)
  │  ├─ Beratung records deleted (1:N)
  │  ├─ Gewalttat records deleted (1:N)
  │  └─ Gewalttat_GewalttatArt junctions deleted
  ├─ Recovery: Not possible (GDPR compliance)
  └─ Use case: DSGVO data deletion requests
```

---

## Implementation Details

### Custom Decorators (`decorators.py`)

```python
@permission_required(permission_name)
def view_function(request, ...):
    # Checks user.role.permissions.{permission_name}
    # Returns 403 if user lacks permission
    # Returns 200 if permitted
```

### Manager Classes (`managers/`)

**FallManager:**
- `createFall(fall_data, personen_data)` - Atomic case creation
- `soft_delete()` - Archive case
- `hard_delete()` - Permanent deletion with CASCADE
- Handles aggregate counter updates

**SessionManager:**
- `add_session()` - Create consultation with auto-aggregates
- `update_session()` - Modify consultation details
- Updates Fall.letzte_beratung and Fall.beratungsanzahl

### Form Validation (`forms/`)

**FallForm:**
- Validates required fields
- Ensures unique aliases
- Date range validation
- Conditional field validation

**GewaltatForm:**
- Conditional field checking
  - If zahl_der_vorfaelle == 'GENAUE_ZAHL' → zahl_der_vorfaelle_genau required
  - If alter_tat_keine_angabe == True → alter field nullable
- M2M violence type selection
- JSON perpetrator details validation

---

## Statistics & Metrics

| Metric | Value |
|--------|-------|
| Core Models | 5 (Fall, PersonenbezogeneDaten, Beratung, Gewalttat, GewalttatArt) |
| User Models | 3 (User, Role, PermissionSet) |
| Views Implemented | 12+ (CRUD + special operations) |
| Forms | 4+ (Case, Consultation, Incident, User) |
| Permission Tiers | 3 (BASIS, ERWEITERT, ADMIN) |
| Database Relations | 8+ (FK, O2O, M2M) |
| Test Cases | 12 comprehensive scenarios |
| Validation Rules | 20+ conditional and field-level rules |

---

*Last Updated: January 7, 2026*
*Phase: 3B (Views & Comprehensive Testing)*
*Repository: WS2025-SE-Bellis-ev*
