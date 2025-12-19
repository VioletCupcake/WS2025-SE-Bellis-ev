# DJANGO BASICS FOR B-EV PROJECT

## What is Django?
Django is a Python web framework that handles:
- Database operations (ORM - Object Relational Mapping)
- URL routing
- User authentication
- Admin interface (auto-generated)
- Form handling and validation

## Core Components

### Models (models.py)
- Define database structure as Python classes
- Each class = database table
- Each attribute = table column
- Django auto-generates SQL

Example:
class Case(models.Model):
    alias = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

### Migrations
- Version control for database schema
- Commands:
  python manage.py makemigrations  # Creates migration files
  python manage.py migrate         # Applies changes to database

### Admin (admin.py)
- Built-in interface for data management
- Register models to make them editable

admin.site.register(Case)

### Views (views.py)
- Handle HTTP requests/responses
- Business logic layer

### URLs (urls.py)
- Route URLs to views
- Map web addresses to functions

## Django Project Structure in B-EV

B_EV/                    # Project configuration folder
├── settings.py          # Database, apps, security settings
├── urls.py              # Main URL routing
├── wsgi.py/asgi.py      # Server deployment

Core/                    # App for core functionality
├── models.py            # Database structure (Cases, Requests, etc.)
├── views.py             # Request handling
├── admin.py             # Admin interface setup
├── migrations/          # Database version history

## Key Django Concepts

### Apps
- Self-contained modules (like "Core" in B-EV)
- Registered in settings.py INSTALLED_APPS

### ORM (Object-Relational Mapping)
Instead of SQL:
  SELECT * FROM case WHERE alias = 'AB123';

Use Python:
  Case.objects.get(alias='AB123')

### Relationships
- ForeignKey: One-to-Many (Case has many Beratungen)
- ManyToManyField: Many-to-Many (Case has many Folgen)
- OneToOneField: One-to-One (User has one Profile)

### QuerySets
- Lazy evaluation (only runs when needed)
- Chainable filters

cases = Case.objects.filter(created_at__year=2025).exclude(deleted=True)
