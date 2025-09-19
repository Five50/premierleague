"""
Custom error views for handling HTTP errors.
"""

from django.shortcuts import render


def custom_404(request, exception=None):
    """Custom 404 error handler."""
    return render(request, "templates/errors/404.html", status=404)


def custom_500(request):
    """Custom 500 error handler."""
    return render(request, "templates/errors/500.html", status=500)


def custom_403(request, exception=None):
    """Custom 403 error handler."""
    return render(request, "templates/errors/403.html", status=403)


def custom_400(request, exception=None):
    """Custom 400 error handler."""
    return render(request, "templates/errors/400.html", status=400)
