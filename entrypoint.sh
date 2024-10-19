#!/bin/sh

# Wait for the database to be ready
echo "Waiting for database..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "Database started"

# Run migrations
echo "Running migrations..."
python manage.py makemigrations
python manage.py migrate

# Create groups
echo "Creating groups..."
python manage.py create_groups

# Setup test data
echo "Setting up test data..."
python manage.py setup_test_data

# Start the main process
echo "Starting main process..."
exec "$@"