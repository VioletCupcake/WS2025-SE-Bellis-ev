# DJANGO MANAGEMENT
python manage.py runserver              # Start development server
python manage.py makemigrations         # Create migration files
python manage.py migrate                # Apply migrations
python manage.py createsuperuser        # Create admin user
python manage.py shell                  # Interactive Python shell with Django
python manage.py dbshell                # Direct database shell

# GIT WORKFLOW
git status                              # Check changes
git pull origin cleanup                 # Get latest code
git checkout -b feature/name            # Create feature branch
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
