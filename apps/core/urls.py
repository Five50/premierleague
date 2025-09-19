from django.urls import path
from django.views.generic import RedirectView
from django.utils.translation import gettext_lazy as _

from . import test_views, views
from apps.shop.views import ShopView as ShopAppView

urlpatterns = [
    # Main pages
    path("", views.HomeView.as_view(), name="home"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("contact/", views.ContactView.as_view(), name="contact"),
    # Services
    path("services/", views.ServicesView.as_view(), name="services"),
    path(
        "physical-therapy/",
        views.PhysicalTherapyView.as_view(),
        name="physical-therapy",
    ),
    path(
        "occupational-therapy/",
        views.OccupationalTherapyView.as_view(),
        name="occupational-therapy",
    ),
    path(
        "massage-therapy/", views.MassageTherapyView.as_view(), name="massage-therapy"
    ),
    path(
        "wellness-programs/",
        views.WellnessProgramsView.as_view(),
        name="wellness-programs",
    ),
    # Products/Shop
    path("products/", views.ProductsView.as_view(), name="products"),
    path("product/single/", views.ProductSingleView.as_view(), name="product-single"),
    path(
        "product/variable/",
        views.ProductVariableView.as_view(),
        name="product-variable",
    ),
    path(
        "product/multi-variable/",
        views.ProductMultiVariableView.as_view(),
        name="product-multi-variable",
    ),
    path(
        "product/<slug:slug>/", views.ProductDetailView.as_view(), name="product-detail"
    ),
    path("checkout/", views.CheckoutView.as_view(), name="checkout"),
    # Blog
    path("blog/", views.BlogView.as_view(), name="blog"),
    path("blog/<slug:slug>/", views.BlogPostView.as_view(), name="blog-post"),
    # Appointments
    path("appointments/", views.AppointmentsView.as_view(), name="appointments"),
    # User authentication
    path("login/", views.LoginView.as_view(), name="login"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path(
        "forgot-password/", views.ForgotPasswordView.as_view(), name="forgot-password"
    ),
    path(
        "reset-password/<uidb64>/<token>/",
        views.ResetPasswordView.as_view(),
        name="reset-password",
    ),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    # Legal and Information Pages
    path("privacy-policy/", views.PrivacyPolicyView.as_view(), name="privacy-policy"),
    path("terms-of-service/", views.TermsOfServiceView.as_view(), name="terms-of-service"),
    path("cookie-policy/", views.CookiePolicyView.as_view(), name="cookie-policy"),
    path("accessibility/", views.AccessibilityView.as_view(), name="accessibility"),
    # Legacy redirects
    path("privacy/", RedirectView.as_view(url="/privacy-policy/", permanent=True), name="privacy"),
    path("terms/", RedirectView.as_view(url="/terms-of-service/", permanent=True), name="terms"),
    # Footer pages (keeping existing ones if they exist)
    path("sitemap/", views.SitemapView.as_view(), name="sitemap"),
    path("insurance/", views.InsuranceView.as_view(), name="insurance"),
    path("careers/", views.CareersView.as_view(), name="careers"),
    # Allsvenskan pages (API-powered)
    path("teams/", views.TeamsView.as_view(), name="teams"),
    path("teams/<slug:team_slug>/", views.TeamDetailView.as_view(), name="team-detail"),
    path("fixtures/", views.FixturesView.as_view(), name="fixtures"),
    path(_("table/"), views.TableView.as_view(), name="table"),  # Swedish: "tabell/"
    path(_("standings/"), views.StandingsView.as_view(), name="standings"),  # Swedish: "tabell/"
    path(_("players/"), views.PlayersView.as_view(), name="players"),  # Swedish: "spelare/"
    path(_("players/") + "<slug:player_slug>/", views.PlayerDetailView.as_view(), name="player-detail"),
    path(_("top-scorers/"), views.TopScorersView.as_view(), name="top-scorers"),  # Swedish: "malskyttar/"
    path(_("assists/"), views.AssistsLeadersView.as_view(), name="assists"),  # Swedish: "assist/"
    path(_("clean-sheets/"), views.CleanSheetsView.as_view(), name="clean-sheets"),  # Swedish: "halla-nollan/"
    path("live/", views.LiveView.as_view(), name="live"),
    path("shop/", ShopAppView.as_view(), name="shop"),
    path("betting/", views.BettingView.as_view(), name="betting"),

    # AJAX API endpoints for live data
    path("api/live-data/", views.LiveDataAPIView.as_view(), name="api-live-data"),
    path("api/standings/", views.StandingsAPIView.as_view(), name="api-standings"),
    path("api/search/", views.SearchAPIView.as_view(), name="api-search"),
    # Test error pages in development
    path("test-errors/404/", test_views.Test404View.as_view(), name="test-404"),
    path("test-errors/500/", test_views.Test500View.as_view(), name="test-500"),
    path("test-errors/403/", test_views.Test403View.as_view(), name="test-403"),
    path("test-errors/400/", test_views.Test400View.as_view(), name="test-400"),
]
