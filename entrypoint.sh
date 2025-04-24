#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Wait for database to be ready - adapt for RDS
echo "Waiting for PostgreSQL (RDS)..."
until PGPASSWORD=$DATABASE_PASSWORD psql -h $DATABASE_HOST -U $DATABASE_USER -d $DATABASE_NAME -c '\q'; do
  >&2 echo "PostgreSQL is unavailable - sleeping"
  sleep 1
done
echo "PostgreSQL is ready"

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Create superuser if needed and doesn't exist
if [ "$DJANGO_SUPERUSER_USERNAME" ] && [ "$DJANGO_SUPERUSER_PASSWORD" ] && [ "$DJANGO_SUPERUSER_EMAIL" ]; then
    echo "Checking for existing superuser..."
    python manage.py shell -c "from django.contrib.auth.models import User; print(User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists())" > /tmp/user_exists
    if grep -q "False" /tmp/user_exists; then
        echo "Creating superuser..."
        python manage.py createsuperuser --noinput
    else
        echo "Superuser already exists."
    fi
fi

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Starting server
echo "Starting server..."
python manage.py runserver 0.0.0.0:8000