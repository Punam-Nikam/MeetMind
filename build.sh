#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Convert static asset files (CSS)
python manage.py collectstatic --no-input

# Apply database migrations (Optional, since you use MongoDB, but keep it)
python manage.py migrate