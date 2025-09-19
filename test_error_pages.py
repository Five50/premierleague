#!/usr/bin/env python
"""
Quick script to test error pages with DEBUG=False
Run this instead of 'python manage.py runserver' to test error pages
"""
import os

if __name__ == "__main__":
    # Set DEBUG=False temporarily
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")
    os.environ["DEBUG"] = "False"

    # Add allowed hosts for testing
    os.environ["ALLOWED_HOSTS"] = "localhost,127.0.0.1,0.0.0.0"

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    print("Starting server with DEBUG=False to test error pages...")
    print("Visit http://127.0.0.1:8000/any-nonexistent-url/ to see the 404 page")

    execute_from_command_line(["manage.py", "runserver"])
