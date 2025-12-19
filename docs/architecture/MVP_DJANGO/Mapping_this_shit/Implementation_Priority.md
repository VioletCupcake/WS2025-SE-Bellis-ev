# RECOMMENDED DEVELOPMENT SEQUENCE (BY FUCKING CLAUDE SONNET 4.5 THINK VIA PERPLEXITY - NOT ME)
# (However at least the beginning makes sense i guess)

PHASE 1: User System
├── models/user_models.py         # User, Role, PermissionSet models
├── migrations/0001_initial.py    # Create tables
├── admin.py                      # Register models for admin interface
└── Test: Create users via admin

PHASE 2: Core Case Structure
├── models/fall_models.py         # Fall, PersonenbezogeneDaten, Beratung
├── migrations/0002_fall_system.py
├── managers/fall_manager.py      # Basic CRUD operations
└── Test: Create cases via admin

PHASE 3: Violence Tracking 
├── models/gewalttat_models.py    # Gewalttat + junction
├── models/reference_models.py    # GewalttatArt reference data
├── migrations/0003_gewalttat.py
└── Test: Add violence incidents to cases

PHASE 4: Consequences & Validation
├── services/validation_service.py
├── Complete reference_models.py  # FolgenDerGewalt
├── migrations/0004_reference_data.py
└── Test: Full case creation with validation

PHASE 5: API Views 
├── views/fall_views.py           # Frontend will connect here
├── serializers/
└── urls.py routing


# KEY STRUCTURAL DECISIONS

## Why Split models.py? I like things together
- Current: All models in single file (acceptable for MVP start)
- Future: Split into domain modules when >500 lines or >8 models
- Trigger point: Either from the start or after Phase 2 completion

## Foreign Key Cascade Rules (from UML Section 07)
Fall → PersonenbezogeneDaten: CASCADE (always delete together)
Fall → Beratung: CASCADE (delete sessions with case)
Fall → Gewalttat: CASCADE (delete incidents with case)
User → Fall: SET_NULL (preserve case if user deactivated)
Role → User: RESTRICT (cannot delete role if users exist)

## Manager vs View Logic
Managers: Database operations, business rules, data integrity
Views: HTTP handling, authentication, response formatting
Rule: If Frontend doesn't trigger it, it belongs in a Manager

## Migration Naming Convention
0001_initial - User/auth system
0002_fall_system - Case management core
0003_gewalttat - Violence tracking
0004_reference_data - Lookup tables
0005_[feature_name] - Subsequent features
