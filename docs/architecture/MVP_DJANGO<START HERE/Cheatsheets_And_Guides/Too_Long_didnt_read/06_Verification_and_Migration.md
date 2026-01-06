# Test database connection
python manage.py check

# Create initial migrations
python manage.py makemigrations

# Apply migrations to PostgreSQL
python manage.py migrate

# Create superuser for admin access
python manage.py createsuperuser

# Run development server
python manage.py runserver

# Access admin at: http://127.0.0.1:8000/admin/



# some VSCode Extensions

1. PostgreSQL (by Chris Kolkman)
   - Query editor
   - Database browser

2. SQLTools (by Matheus Teixeira)
   - Universal database interface
   - Visual query builder

## Connection Setup in SQLTools

1. Install SQLTools + PostgreSQL driver
2. Open Command Palette (Ctrl+Shift+P)
3. "SQLTools: Add New Connection"
4. Select PostgreSQL
5. Enter:
   - Connection Name: BEV-Local
   - Server: localhost
   - Port: 5432
   - Database: bev_db
   - Username: bev_user
   - Password: [your password]

## Or something like that