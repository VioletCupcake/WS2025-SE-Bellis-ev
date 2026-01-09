#!/bin/bash
# B-EV Docker Entrypoint Script
# Handles database setup and Django server startup

# Exit on error, but with custom handling
set -e

# Error handler function
error_handler() {
    echo ""
    echo "!!! ERROR: Script failed at line $1 !!!"
    echo "!!! Last command exit code: $2 !!!"
    echo ""
    echo "=== TROUBLESHOOTING ==="
    echo "1. Database connection failed?"
    echo "   - Check if PostgreSQL container is running: docker ps"
    echo "   - Check DB logs: docker logs bev-postgres"
    echo "   - Verify environment variables: DB_HOST=$DB_HOST, DB_PORT=$DB_PORT"
    echo ""
    echo "2. Migration failed?"
    echo "   - Check for model errors in Django code"
    echo "   - Try: docker compose down -v && docker compose up --build"
    echo ""
    echo "3. Fixture loading failed?"
    echo "   - Verify seed_data.json exists and is valid JSON"
    echo "   - Check for UUID/foreign key conflicts"
    echo ""
    exit 1
}

trap 'error_handler $LINENO $?' ERR

echo "=== B-EV MVP Case Management System ==="
echo "Starting container initialization..."
echo "yay for progress displays"

# Validate required environment variables
echo "[1/5] Validating environment variables..."
MISSING_VARS=""
[ -z "$DB_NAME" ] && MISSING_VARS="$MISSING_VARS DB_NAME"
[ -z "$DB_USER" ] && MISSING_VARS="$MISSING_VARS DB_USER"
[ -z "$DB_PASSWORD" ] && MISSING_VARS="$MISSING_VARS DB_PASSWORD"
[ -z "$DB_HOST" ] && MISSING_VARS="$MISSING_VARS DB_HOST"

if [ -n "$MISSING_VARS" ]; then
    echo "!!! FATAL: Missing required environment variables:$MISSING_VARS"
    echo "!!! Ensure docker-compose.yml defines all DB_* variables"
    exit 1
fi
echo "    Environment variables OK"

# Wait for database to be ready
echo "[2/5] Waiting for PostgreSQL at $DB_HOST:$DB_PORT..."
MAX_RETRIES=30
RETRY_COUNT=0
while ! python -c "import psycopg2; psycopg2.connect(dbname='$DB_NAME', user='$DB_USER', password='$DB_PASSWORD', host='$DB_HOST', port='$DB_PORT')" 2>/dev/null; do
    RETRY_COUNT=$((RETRY_COUNT + 1))
    if [ $RETRY_COUNT -ge $MAX_RETRIES ]; then
        echo "!!! FATAL: Database connection timeout after $MAX_RETRIES attempts"
        echo "!!! Check PostgreSQL container status and credentials"
        exit 1
    fi
    echo "    Attempt $RETRY_COUNT/$MAX_RETRIES - Database not ready, waiting..."
    sleep 2
done
echo "    PostgreSQL connection established!"

# Run migrations
echo "[3/5] Applying database migrations..."
if ! python manage.py migrate --noinput 2>&1; then
    echo "!!! FATAL: Migration failed"
    echo "!!! Check Django model definitions and migration files"
    exit 1
fi
echo "    Migrations applied successfully"

# Load seed data only if no users exist (first run)
echo "[4/5] Checking seed data..."
USER_COUNT=$(python manage.py shell -c "from core.models import User; print(User.objects.count())" 2>/dev/null || echo "ERROR")

if [ "$USER_COUNT" = "ERROR" ]; then
    echo "!!! WARNING: Could not query user count, attempting seed anyway..."
    USER_COUNT=0
fi

if [ "$USER_COUNT" -eq "0" ]; then
    echo "    No users found, loading seed data..."
    if ! python manage.py loaddata core/fixtures/seed_data.json 2>&1; then
        echo "!!! FATAL: Failed to load seed data"
        echo "!!! Check seed_data.json for valid JSON and correct model references"
        exit 1
    fi
    echo "    Seed data loaded successfully!"
else
    echo "    Database already seeded ($USER_COUNT users found), skipping..."
fi

# Start server
echo "[5/5] Starting Django server..."
echo ""
echo "============================================="
echo "   B-EV Case Management System READY"
echo "============================================="
echo ""
echo "   URL: http://localhost:8002/login/"
echo "   ADMIN URL: http://localhost:8002/admin/"
echo ""
echo "   Test Accounts (password: test123):"
echo "     - user_basis     (BASIS role)"
echo "     - user_erweitert (ERWEITERT role)"
echo "     - user_admin     (ADMIN role)"
echo ""
echo "   Press Ctrl+C to stop the server"
echo "============================================="
echo ""

# Start Django development server
exec python manage.py runserver 0.0.0.0:8002
