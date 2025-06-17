#!/usr/bin/env bash
# exit on error
set -o errexit

# Install Python dependencies
pip install -r requirements.txt

# Create necessary directories
mkdir -p staticfiles
mkdir -p media

# Set proper permissions
chmod -R 755 static
chmod -R 755 staticfiles
chmod -R 755 media

# Collect static files
python manage.py collectstatic --no-input --clear

# Apply database migrations
python manage.py migrate 