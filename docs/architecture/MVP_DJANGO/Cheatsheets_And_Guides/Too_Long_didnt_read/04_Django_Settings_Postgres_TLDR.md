# B_EV/settings.py

# REPLACE THIS (default SQLite):
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# WITH THIS (PostgreSQL):
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'bev_db',
        'USER': 'bev_user',
        'PASSWORD': 'secure_password_here',  # Use environment variable in production
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# RECOMMENDED: Environment Variables for Security
# Install python-decouple:
# pip install python-decouple

from decouple import config

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='bev_db'),
        'USER': config('DB_USER', default='bev_user'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}
