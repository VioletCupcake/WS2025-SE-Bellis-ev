# SWITCHING DJANGO FROM SQLITE TO POSTGRESQL

## Why PostgreSQL?
- Production-grade database
- Better concurrency handling
- Advanced features (JSON fields, full-text search)
- Required for B-EV deployment

## Installation

### Linux Mint (idfk how you do that on windows, go google)
sudo apt update
sudo apt install postgresql postgresql-contrib libpq-dev
sudo systemctl start postgresql
sudo systemctl enable postgresql

### Create Database and User
sudo -u postgres psql

# In PostgreSQL prompt:
CREATE DATABASE bev_db;
CREATE USER bev_user WITH PASSWORD 'secure_password_here'; 
ALTER ROLE bev_user SET client_encoding TO 'utf8';
ALTER ROLE bev_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE bev_user SET timezone TO 'Europe/Berlin';
GRANT ALL PRIVILEGES ON DATABASE bev_db TO bev_user;
\q

## Python PostgreSQL Adapter

### Install psycopg2
pip install psycopg2-binary

### Update requirements.txt
echo "psycopg2-binary==2.9.9" >> requirements.txt
