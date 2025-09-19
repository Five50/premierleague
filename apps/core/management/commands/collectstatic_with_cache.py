"""
Management command to collect static files with cache busting
"""

from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Collect static files with cache busting for production"

    def handle(self, *args, **options):
        self.stdout.write("Collecting static files with cache busting...")

        # First, collect static files normally
        call_command("collectstatic", "--noinput", "--clear")

        self.stdout.write(self.style.SUCCESS("Successfully collected static files"))

        # Add cache busting info
        self.stdout.write(
            """
Cache Configuration Summary:
============================
Images (.jpg, .png, .webp, .svg): 30 days
Minified CSS/JS (.min.css, .min.js): 7 days
Regular CSS/JS: 1 day
Fonts (.woff, .woff2): 30 days

WhiteNoise will automatically:
- Compress files with gzip
- Add unique hashes to filenames
- Serve with proper cache headers

To ensure cache busting works:
1. Use {% static %} template tag for all assets
2. Run collectstatic before deployment
3. WhiteNoise will handle the rest!
        """
        )
