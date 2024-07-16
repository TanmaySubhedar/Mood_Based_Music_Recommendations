#!/bin/sh

# Use the Python interpreter provided by Vercel
python3.9 -m pip install -r requirements.txt

# Collect static files
python3.9 manage.py collectstatic --noinput

# Run database migrations
python3.9 manage.py migrate
