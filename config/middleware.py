"""
Security middleware for modern web standards
"""

import re

from django.utils import translation
from django.utils.cache import patch_cache_control


class SecurityHeadersMiddleware:
    """Add security headers to responses"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Content Security Policy
        csp_directives = [
            "default-src 'self'",
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://d3js.org",  # Alpine.js requires unsafe-eval, D3.js from CDN
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com",
            "img-src 'self' data: https:",
            "font-src 'self' https://fonts.gstatic.com",
            "connect-src 'self'",
            "frame-ancestors 'none'",
            "base-uri 'self'",
            "form-action 'self'",
        ]
        response["Content-Security-Policy"] = "; ".join(csp_directives)

        # Other security headers
        response["X-Content-Type-Options"] = "nosniff"
        response["X-Frame-Options"] = "DENY"
        response["X-XSS-Protection"] = "1; mode=block"
        response["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"

        # HSTS is handled by Django's SecurityMiddleware

        return response


class LanguageFromURLMiddleware:
    """Set language based on URL path for better control."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if path starts with /en/ for English
        if request.path.startswith("/en/"):
            translation.activate("en")
            request.LANGUAGE_CODE = "en"
        else:
            # Default to Swedish for Premier League Swedish site
            translation.activate("sv")
            request.LANGUAGE_CODE = "sv"

        response = self.get_response(request)
        return response


class CacheControlMiddleware:
    """Add cache control headers for static assets"""

    # File patterns that should be cached for a long time
    CACHE_PATTERNS = [
        # Images - 1 year (they rarely change)
        (r"\.(jpg|jpeg|png|gif|webp|svg|ico)$", 31536000),
        # Minified CSS and JS - 1 year (versioned files)
        (r"\.min\.(css|js)$", 31536000),
        # Regular CSS and JS - 1 week
        (r"\.(css|js)$", 604800),
        # Fonts - 1 year
        (r"\.(woff|woff2|eot|ttf|otf)$", 31536000),
        # PDFs and documents - 1 month
        (r"\.(pdf|doc|docx|xls|xlsx)$", 2592000),
    ]

    def __init__(self, get_response):
        self.get_response = get_response
        self.compiled_patterns = [
            (re.compile(pattern, re.IGNORECASE), max_age)
            for pattern, max_age in self.CACHE_PATTERNS
        ]

    def __call__(self, request):
        response = self.get_response(request)

        # Add cache headers for static and media files
        if request.path.startswith("/static/") or request.path.startswith("/media/"):
            # Check each pattern in order (first match wins)
            for pattern, max_age in self.compiled_patterns:
                if pattern.search(request.path):
                    # Set cache control headers
                    patch_cache_control(
                        response,
                        max_age=max_age,
                        public=True,
                        immutable=True if max_age >= 31536000 else False,
                    )
                    # Add Vary header for better caching
                    if "Vary" in response:
                        if "Accept-Encoding" not in response["Vary"]:
                            response["Vary"] += ", Accept-Encoding"
                    else:
                        response["Vary"] = "Accept-Encoding"

                    # Add explicit Expires header for older browsers
                    import time

                    from django.utils.http import http_date

                    response["Expires"] = http_date(time.time() + max_age)
                    break

        return response


class CompressionMiddleware:
    """Ensure compression headers are properly set for all responses"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Add Vary header to ensure proper caching with compression
        if "Vary" in response:
            if "Accept-Encoding" not in response["Vary"]:
                response["Vary"] += ", Accept-Encoding"
        else:
            response["Vary"] = "Accept-Encoding"

        # For HTML responses, ensure they're compressed
        content_type = response.get("Content-Type", "")
        if "text/html" in content_type or "application/json" in content_type:
            # Django's GZipMiddleware will handle the actual compression
            # We just ensure the headers are set correctly
            response["Cache-Control"] = "no-cache, must-revalidate"

        return response
