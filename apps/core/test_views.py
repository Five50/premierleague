"""
Test views for viewing error pages in development.
"""

from django.shortcuts import render
from django.views.generic import TemplateView


class Test404View(TemplateView):
    """Test 404 error page in development."""

    template_name = "404.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, status=404)


class Test500View(TemplateView):
    """Test 500 error page in development."""

    template_name = "500.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, status=500)


class Test403View(TemplateView):
    """Test 403 error page in development."""

    template_name = "403.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, status=403)


class Test400View(TemplateView):
    """Test 400 error page in development."""

    template_name = "400.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, status=400)
