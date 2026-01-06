# DJANGO MANAGEMENT
# Start development server
python manage.py runserver 
            
# Create new migration (auto-numbered)
python manage.py makemigrations
# Create migration with custom name
python manage.py makemigrations --name your_description
# Show which migrations are applied
python manage.py showmigrations
# Preview SQL for specific migration
python manage.py sqlmigrate <app> <migration_number>
# Apply all pending migrations
python manage.py migrate
# Roll back to specific migration
python manage.py migrate core 0005  # reverts 0006
# Check for issues without making changes
python manage.py check

python manage.py createsuperuser        # Create admin user
python manage.py shell                  # Interactive Python shell with Django
python manage.py dbshell                # Direct database shell

# GIT WORKFLOW
git status                              # Check changes
git pull origin cleanup                 # Get latest code
git checkout -b feature/name            # Create feature branch, or move without -b
git add .                               # Stage all changes
git commit -m "Message"                 # Commit changes
git push origin feature/name            # Push to GitHub

# POSTGRESQL
sudo systemctl status postgresql        # Check if running
sudo systemctl start postgresql         # Start database
sudo -u postgres psql                   # Access PostgreSQL prompt
\l                                      # List databases
\c bev_db                               # Connect to database
\dt                                     # Show tables
\q                                      # Quit
