# Repository Structure - ASCII Tree

This document provides a complete visual representation of the WS2025-SE-Bellis-ev repository structure.

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
│       ├── models.py                # Legacy models.py (redirects to models/ package)
│       ├── views.py                 # Django views
│       ├── tests.py                 # Unit tests
│       ├── fixtures/                # JSON fixtures for test data
│       │   └── (empty, for JSON data files)
│       │
│       ├── forms/                   # Django forms package
│       │   ├── __init__.py
│       │   ├── fall_forms.py         # Fall/Gewalttat-related forms
│       │   └── user_forms.py         # User-related forms
│       │
│       ├── managers/                # Custom managers and services
│       │   ├── __init__.py
│       │   ├── fall_manager.py       # Fall management logic
│       │   └── session_manager.py    # Session/consultation management
│       │
│       ├── models/                  # Modular models package
│       │   ├── __init__.py           # Aggregates imports from submodules
│       │   ├── fall_models.py        # Fall, PersonenbezogeneDaten, Beratung, Gewalttat
│       │   ├── user_models.py        # User-related models
│       │   └── reference_models.py   # Reference data models (GewalttatArt, etc.)
│       │
│       ├── services/                # Business logic services
│       │   ├── __init__.py
│       │   └── validation_service.py # Core validation logic
│       │
│       ├── templates/               # HTML templates
│       │   └── core/                # Templates for core app
│       │       └── (empty, for HTML files)
│       │
│       └── migrations/              # Database migrations
│           └── __init__.py
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
| `docs/STYLEGUIDE.md` | Documentation style guidelines |
| `docs/architecture/MVP_Definition.md` | MVP scope and definitions |
| `src/manage.py` | Django project management interface |
| `src/B_EV/settings.py` | Django project settings and configuration |

## Statistics

- **Total Directories:** 134
- **Total Files:** 193
- **Main Source Directories:** 2 (B_EV, core)
- **Documentation Sections:** 6+ major categories

---

*Generated: January 3, 2026*
*Repository: WS2025-SE-Bellis-ev*
