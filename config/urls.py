"""
URL Configuration for theme_dev project.
"""

from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

# Non-internationalized URLs
urlpatterns = [
    path("admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),  # Language switching
]

# Internationalized URLs
urlpatterns += i18n_patterns(
    path("", include("apps.core.urls")),
    path("cart/", include("apps.cart.urls")),
    path("shop/", include("apps.shop.urls")),
    prefix_default_language=False,  # Don't prefix default language (Swedish)
)

# Serve media files during development
# Note: Static files are served by WhiteNoise middleware
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Don't add static() for STATIC_URL - let WhiteNoise handle it

# Custom error handlers
handler404 = "apps.core.error_views.custom_404"
handler500 = "apps.core.error_views.custom_500"
handler403 = "apps.core.error_views.custom_403"
handler400 = "apps.core.error_views.custom_400"
