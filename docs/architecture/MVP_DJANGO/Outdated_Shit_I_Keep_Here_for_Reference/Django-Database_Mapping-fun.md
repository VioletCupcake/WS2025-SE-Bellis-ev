
#### UML to Django Mapping Explanation 

============================================================================
## MAPPING OUR MVP UML TO DJANGO
## What Django Gives You vs. What You Need to Write
## Repository: https://github.com/VXXXXtCXXXXXke/WS2025-SE-B-ev/
## Working Branch: cleanup
============================================================================

## INTRODUCTION

Our UML diagrams show the WHAT (entities, relationships, methods).
Django provides the HOW (implementation patterns and shortcuts).

This guide shows you:
- What Django does automatically (90% of infrastructure)
- What you need to write (10% business logic)
- Where each component lives in the codebase

## YOUR PROJECT STRUCTURE EXPLAINED

src/
├── B_EV/           # Django PROJECT (settings, configuration)
│ ├── settings.py   # Database config, installed apps, middleware
│ ├── urls.py       # Main URL routing (delegates to apps)
│ ├── wsgi.py       # Web server gateway (production)
│ └── asgi.py       # Async server (WebSockets, etc.)
│
├── Core/           # Django APP (first app, possibly for shared models)
│ ├── models.py     # Database models (Fall, Beratung, etc.)
│ ├── views.py      # HTTP request handlers
│ ├── urls.py       # App-specific URL routing
│ ├── admin.py      # Admin interface config
│ ├── forms.py      # Form definitions (create this)
│ ├── managers.py   # FallManager business logic (create this)
│ ├── services.py   # ValidationService utilities (create this)
│ ├── tests.py      # Unit tests
│ └── migrations/   # Database schema versions (auto-generated)
│
├── manage.py       # Django command-line tool
└── README.md       # Project setup instructions

Future structure (you'll create these):
├── users/          # User authentication app
│ ├── models.py     # User, Role models
│ └── ...
├── cases/          # Case management app (might merge with Core)
│ ├── models.py     # Fall, Beratung, Gewalttat
│ └── ...
└── reference_data/ # GewalttatArt, FolgenDerGewalt
├── models.py
└── ...


**Decision Point:** Should Case models go in `Core/` or new `cases/` app?

**Recommendation for MVP:** Keep everything in `Core/` for simplicity.
Split into separate apps post-MVP when codebase grows. (Or do it from the start, so we dont have to split all the shit up later, because this part here is literally a suggestion by claude and i cant be bothered to rework it right now)

## MAPPING OVERVIEW TABLE

| UML Component         | Django Solution                           | Automatic?                | Files Involved |
|---------------        |-----------------                          |------------               |----------------|
| User entity           | django.contrib.auth.models.AbstractUser   | 95% auto                  | users/models.py |
| Session entity        | django.contrib.sessions                   | 100% auto                 | (built-in) |
| Role + PermissionSet  | Groups + Permissions                      | 90% auto                  | users/models.py |
| Fall, Beratung, Gewalttat | models.Model subclasses               | Manual definition, auto DB | Core/models.py |
| Foreign keys          | ForeignKey field                          | Auto relationship         | Core/models.py |
| Many-to-many          | ManyToManyField                           | Auto junction table       | Core/models.py |
| Cascade delete        | on_delete parameter                       | Auto enforcement          | Core/models.py |
| Enums                 | CharField(choices=...)                    | Auto validation           | Core/models.py |
| JSON fields           | JSONField                                 | Auto storage              | Core/models.py |
| ValidationService     | Form.clean_*() methods                    | Manual logic              | Core/forms.py |
| FallManager           | Custom class                              | 100% manual               | Core/managers.py |
| Search methods        | QuerySet API                              | Manual logic, auto SQL    | Core/views.py |
| Admin UI              | django.contrib.admin                      | 95% auto                  | Core/admin.py |

**Pattern:** Django handles infrastructure (database, auth, forms).
You write business logic (FallManager, custom validation).

## DETAILED MAPPING BY UML SECTION

## ============================================================================
## SECTION 1: USER & PERMISSION SYSTEM (90% Django Built-in)
## ============================================================================

### UML Says:
User:

    user_id : string {PK}

    username : string

    email : string

    password_hash : string

    is_active : boolean

    created_at : datetime

    role_id : string {FK → Role}

    login(username, password) : Session

    logout(session_id) : void

    changePassword(old, new) : boolean

Session:

    session_id : string {PK}

    user_id : string {FK}

    start_time : datetime

    last_activity : datetime

    is_active : boolean

Role:

    role_id : string {PK}

    name : enum<BASIS, ERWEITERT, ADMINISTRATOR>

    description : text

PermissionSet:

    permission_set_id : string {PK}

    role_id : string {FK}

    can_view_cases : boolean

    can_edit_cases : boolean

    can_delete_cases : boolean

    can_manage_reference_data : boolean

    can_manage_users : boolean

    can_assign_roles : boolean


### Django Provides:

**✅ User Model (95% built-in)**

File: `src/users/models.py` (create this app)
