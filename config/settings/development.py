"""
Development settings for theme_dev project.

This file contains settings specific to development environment.
"""

from decouple import config

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default=True, cast=bool)

ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS", default="localhost,127.0.0.1,www.localhost,testserver"
).split(",")

# Development-specific apps
INSTALLED_APPS += [
    # Django Debug Toolbar (install with: pip install django-debug-toolbar)
    # 'debug_toolbar',
    # Django Extensions
    # 'django_extensions',
]

# Development-specific middleware
MIDDLEWARE += [
    # Debug toolbar middleware (should be last)
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
]

# Debug toolbar configuration
DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": lambda request: DEBUG,
}

# Internal IPs for debug toolbar
INTERNAL_IPS = [
    "127.0.0.1",
    "localhost",
]

# Database for development (can override for PostgreSQL)
if config("DATABASE_URL", default="").startswith("postgres"):
    import dj_database_url

    DATABASES["default"] = dj_database_url.parse(config("DATABASE_URL"))
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# Email backend for development
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Cache configuration for development
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}

# WhiteNoise settings for development (override production caching)
# Reasonable cache times for development testing
WHITENOISE_MAX_AGE = 3600  # 1 hour in development (enough for testing)
WHITENOISE_AUTOREFRESH = True  # Auto-refresh static files in development


# Override specific cache times for different file types in development
def WHITENOISE_IMMUTABLE_FILE_TEST(path, url):
    return False  # Disable immutable in dev


# Disable HTTPS redirects in development
SECURE_SSL_REDIRECT = False
SECURE_HSTS_SECONDS = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# Development logging - quieter for better development experience
LOGGING["handlers"]["console"]["level"] = "INFO"
LOGGING["loggers"]["django"]["level"] = "WARNING"
LOGGING["loggers"]["django.db.backends"] = {
    "handlers": ["console"],
    "level": "WARNING",  # Suppress SQL queries
    "propagate": False,
}

# Create logs directory if it doesn't exist
import os

os.makedirs(BASE_DIR / "logs", exist_ok=True)
