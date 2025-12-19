### So since we had some, like, issues with understanding where shit goes within the github repo, i made you all this
### Its meant to visualise the Repository structure WITH Implementation Mapping
### This means this is a way this repo COULD look like. It is NOT a definitive final structure

WS2025-SE-B-ev/
│
├── .github/                              # GitHub Actions CI/CD configuration (if we do it)
│   └── workflows/                        # Automated testing and deployment pipelines
│
├── docs/                                 # Project documentation
│   ├── architecture/                     # Design artifacts
│   │   ├── FULL_UML/                    # Complete system design (reference only)
│   │   ├── MVP_UML/                     # Minimal viable product design (current phase)
│   │   └── MVP_DJANGO/                  # Django implementation guides
│   │       └── Cheatsheets_and_Guides/  # Backend team reference material
│   ├── team_documentation/              # Internal team guides and meeting notes
│   └── user_documentation/              # End-user manuals and help guides
│
├── src/                                  # Application source code
│   │
│   ├── B_EV/                            # Django project configuration (root settings)
│   │   ├── __pycache__/                 # Python bytecode cache (ignored by git)
│   │   ├── __init__.py                  # Python package marker
│   │   ├── asgi.py                      # ASGI server entry point (async deployment)
│   │   ├── settings.py                  # *** MAIN CONFIG: Database, apps, middleware, security ***
│   │   ├── urls.py                      # *** ROOT URL ROUTING: Maps URLs to app views ***
│   │   └── wsgi.py                      # WSGI server entry point (standard deployment)
│   │
│   ├── Core/                            # Main application module (all business logic)
│   │   │
│   │   ├── migrations/                  # Database version control
│   │   │   ├── __init__.py             # Package marker
│   │   │   ├── 0001_initial.py         # [FUTURE] Initial schema: User, Role, PermissionSet
│   │   │   ├── 0002_fall_system.py     # [FUTURE] Fall, PersonenbezogeneDaten, Beratung
│   │   │   ├── 0003_gewalttat.py       # [FUTURE] Gewalttat and related tables
│   │   │   └── 0004_reference_data.py  # [FUTURE] GewalttatArt, FolgenDerGewalt, junctions
│   │   │
│   │   ├── models/                      # [FUTURE] Database models (split for maintainability)
│   │   │   ├── __init__.py             # Exports all models for imports
│   │   │   ├── user_models.py          # User, Session, Role, PermissionSet
│   │   │   ├── fall_models.py          # Fall, PersonenbezogeneDaten, Beratung
│   │   │   ├── gewalttat_models.py     # Gewalttat, Gewalttat_GewalttatArt
│   │   │   └── reference_models.py     # GewalttatArt, FolgenDerGewalt, Fall_FolgenDerGewalt
│   │   │
│   │   ├── managers/                    # [FUTURE] Business logic coordinators
│   │   │   ├── __init__.py             
│   │   │   ├── fall_manager.py         # FallManager: createFall, addBeratung, searchByAlias
│   │   │   └── session_manager.py      # SessionManager: login, logout, validateSession
│   │   │
│   │   ├── services/                    # [FUTURE] Utility services
│   │   │   ├── __init__.py
│   │   │   └── validation_service.py   # ValidationService: validateInput, validateDate
│   │   │
│   │   ├── views/                       # [FUTURE] HTTP request handlers (split by domain)
│   │   │   ├── __init__.py
│   │   │   ├── fall_views.py           # Case CRUD endpoints
│   │   │   ├── beratung_views.py       # Counseling session endpoints
│   │   │   └── auth_views.py           # Login/logout endpoints
│   │   │
│   │   ├── serializers/                 # [FUTURE] Data validation and API serialization
│   │   │   ├── __init__.py
│   │   │   ├── fall_serializers.py
│   │   │   └── user_serializers.py
│   │   │
│   │   ├── urls.py                      # [FUTURE] Core app URL routing
│   │   │
│   │   ├── __init__.py                  # Package marker
│   │   ├── admin.py                     # *** CURRENT: Admin interface registration ***
│   │   ├── apps.py                      # App configuration (registered in settings.py)
│   │   ├── models.py                    # *** CURRENT: All models (will be split into models/) ***
│   │   ├── tests.py                     # Unit and integration tests
│   │   └── views.py                     # *** CURRENT: All views (will be split into views/) ***
│   │
│   └── manage.py                        # Django CLI entry point (runserver, migrate, etc.)
│
├── .dockerignore                        # Exclude files from Docker image
├── .gitignore                           # Exclude files from git (*.pyc, .env, __pycache__)
├── .env                                 # [FUTURE] Environment variables (DB credentials, SECRET_KEY)
├── requirements.txt                     # Python dependencies (Django, psycopg2, etc.)
├── Dockerfile                           # [FUTURE] Container definition
├── docker-compose.yml                   # [FUTURE] Multi-container orchestration (Django + Postgres)
└── README.md                            # Project overview and setup instructions
