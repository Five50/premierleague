import logging
import json
import os
from django.shortcuts import redirect
from django.views.generic import TemplateView, View
from django.contrib import messages
from django.utils.translation import gettext as _
from django.http import JsonResponse
from django.conf import settings
from django.core.mail import send_mail
from .services.api_football import api_football_service, APIFootballError

logger = logging.getLogger(__name__)


class HomeView(TemplateView):
    """Home page view with live Allsvenskan data"""

    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "ALLSVENSKAN Insikter - Swedish Football Statistics & Tables"

        try:
            # Get live data for home page
            context["standings"] = api_football_service.get_standings()[:10]  # Top 10 teams for table
            context["top_scorers"] = api_football_service.get_top_scorers(limit=10)
            context["recent_fixtures"] = api_football_service.get_fixtures(status='FT', last=5)
            context["upcoming_fixtures"] = api_football_service.get_fixtures(status='NS', next=5)
            context["live_matches"] = api_football_service.get_live_fixtures()

            # Additional data for tabbed section
            try:
                context["top_assists"] = api_football_service.get_top_assists(limit=5)
            except Exception as e:
                logger.warning(f"Could not load top assists: {e}")
                context["top_assists"] = []

            # Get goalkeeper clean sheets data (from top scorers but filter goalkeepers)
            try:
                all_players = api_football_service.get_top_scorers(limit=50)
                clean_sheets_data = []
                for player in all_players:
                    position = player.get('statistics', [{}])[0].get('games', {}).get('position', '')
                    if position and 'keeper' in position.lower():
                        clean_sheets_data.append(player)
                context["clean_sheets"] = clean_sheets_data[:5]
            except Exception as e:
                logger.warning(f"Could not load clean sheets data: {e}")
                context["clean_sheets"] = []

            context["api_data_available"] = True
            logger.info("Successfully loaded home page with live API data")

        except APIFootballError as e:
            logger.error(f"Failed to load API data for home page: {e}")
            # Provide fallback empty data
            context["standings"] = []
            context["top_scorers"] = []
            context["recent_fixtures"] = []
            context["upcoming_fixtures"] = []
            context["live_matches"] = []
            context["top_assists"] = []
            context["clean_sheets"] = []
            context["api_data_available"] = False

        except Exception as e:
            logger.error(f"Unexpected error loading home page API data: {e}")
            context["standings"] = []
            context["top_scorers"] = []
            context["recent_fixtures"] = []
            context["upcoming_fixtures"] = []
            context["live_matches"] = []
            context["top_assists"] = []
            context["clean_sheets"] = []
            context["api_data_available"] = False

        return context


# Main Pages
class AboutView(TemplateView):
    """About page view"""

    template_name = "pages/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "About Us - Wellness & Rehab Center"
        return context


class ContactView(TemplateView):
    """Contact page view"""

    template_name = "pages/contact.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Contact Us - Wellness & Rehab Center"
        return context


# Services Views
class ServicesView(TemplateView):
    """Services listing page"""

    template_name = "pages/services.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Our Services - Wellness & Rehab Center"
        return context


class PhysicalTherapyView(TemplateView):
    """Physical therapy service page"""

    template_name = "pages/services/physical-therapy.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Physical Therapy - Wellness & Rehab Center"
        return context


class OccupationalTherapyView(TemplateView):
    """Occupational therapy service page"""

    template_name = "pages/services/occupational-therapy.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Occupational Therapy - Wellness & Rehab Center"
        return context


class MassageTherapyView(TemplateView):
    """Massage therapy service page"""

    template_name = "pages/services/massage-therapy.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Massage Therapy - Wellness & Rehab Center"
        return context


class WellnessProgramsView(TemplateView):
    """Wellness programs page"""

    template_name = "pages/services/wellness-programs.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Wellness Programs - Wellness & Rehab Center"
        return context


# Products/Shop Views
class ProductsView(TemplateView):
    """Products listing page"""

    template_name = "pages/products.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Shop Wellness Products - Wellness & Rehab Center"
        # In a real app, you would fetch products from the database
        context["products"] = []
        return context


class ProductDetailView(TemplateView):
    """Dynamic product detail page that routes to appropriate template based on product type"""

    def get_template_names(self):
        """Dynamically select template based on product characteristics"""
        # In a real app, you would fetch the product by slug from the database
        # For now, we'll use the slug from URL to demonstrate different product types
        product_slug = self.kwargs.get('slug', '')
        
        # Classify products based on their characteristics
        # Multi-variable products: complex items with multiple variation options (shirts/kits with sizes, colors)
        multi_variable_products = [
            'arsenal-home-kit-2024-25',
            'manchester-city-home-kit-2024-25', 
            'manchester-united-away-kit-2024-25',
            'chelsea-away-kit-2024-25',
            'chelsea-third-kit-2024-25',
            'tottenham-home-kit-2024-25',
            'liverpool-third-kit-2024-25',
            'liverpool-home-kit-kids-2024-25',
            'tottenham-away-kit-2023-24',
        ]
        
        # Variable products: items with one main variation (retro items with limited sizes)
        variable_products = [
            'manchester-united-retro-kit-1999',
            'arsenal-retro-kit-2003-04-invincibles',
            'liverpool-champions-league-shirt-2019',
            'arsenal-training-jacket',
            'manchester-city-training-shorts',
        ]
        
        # Single products: simple items with no major variations
        single_products = [
            'premier-league-official-match-ball',
            'arsenal-vintage-scarf',
            'premier-league-goalkeeper-gloves',
            'chelsea-polo-shirt',
            'premier-league-referee-kit',
            'premier-league-training-cones-set',
        ]
        
        # Determine template based on product classification
        if any(slug in product_slug for slug in multi_variable_products):
            return ["pages/product-multi-variable.html"]
        elif any(slug in product_slug for slug in variable_products):
            return ["pages/product-variable.html"]
        else:
            return ["pages/product-single.html"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_slug = self.kwargs.get('slug', '')
        
        # Set appropriate page title based on product
        if 'arsenal' in product_slug:
            context["page_title"] = "Arsenal Kit - Premier League Shop"
        elif 'manchester-city' in product_slug:
            context["page_title"] = "Manchester City Kit - Premier League Shop"
        elif 'manchester-united' in product_slug:
            context["page_title"] = "Manchester United Kit - Premier League Shop"
        elif 'chelsea' in product_slug:
            context["page_title"] = "Chelsea Kit - Premier League Shop"
        elif 'tottenham' in product_slug:
            context["page_title"] = "Tottenham Kit - Premier League Shop"
        elif 'liverpool' in product_slug:
            context["page_title"] = "Liverpool Kit - Premier League Shop"
        elif 'ball' in product_slug:
            context["page_title"] = "Official Premier League Ball - Premier League Shop"
        else:
            context["page_title"] = "Premier League Product - Premier League Shop"
        
        # In a real app, you would fetch the actual product data by slug
        context["product"] = {}
        return context


class ProductSingleView(TemplateView):
    """Single product template - simple product with no variations"""

    template_name = "pages/product-single.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Premium Meditation Cushion - Miami Elite Rehab"
        return context


class ProductVariableView(TemplateView):
    """Variable product template - product with one variation option"""

    template_name = "pages/product-variable.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Recovery Supplement Pack - Miami Elite Rehab"
        return context


class ProductMultiVariableView(TemplateView):
    """Multi-variable product template - product with multiple variation options"""

    template_name = "pages/product-multi-variable.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Professional Yoga Mat - Miami Elite Rehab"
        return context


class CartView(TemplateView):
    """Shopping cart page"""

    template_name = "pages/cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Shopping Cart - Wellness & Rehab Center"
        context["cart_items"] = []
        return context


class CheckoutView(TemplateView):
    """Checkout page"""

    template_name = "pages/checkout.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Checkout - Wellness & Rehab Center"
        return context


# Blog Views
class BlogView(TemplateView):
    """Blog listing page"""

    template_name = "pages/blog.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Blog - Wellness & Rehab Center"
        # In a real app, you would fetch blog posts from the database
        context["blog_posts"] = []
        return context


class BlogPostView(TemplateView):
    """Single blog post page"""

    template_name = "pages/blog-post.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # In a real app, you would fetch the blog post by slug from the database
        context["page_title"] = "Blog Post Title - Wellness & Rehab Center"
        context["post"] = {}
        return context


# Appointments
class AppointmentsView(TemplateView):
    """Appointments booking page"""

    template_name = "pages/appointments.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Book Appointment - Wellness & Rehab Center"
        return context


# User Authentication Views
class LoginView(TemplateView):
    """Login page - simplified version"""

    template_name = "pages/login.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Login - Wellness & Rehab Center"
        return context


class RegisterView(TemplateView):
    """Registration page"""

    template_name = "pages/register.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Register - Wellness & Rehab Center"
        return context


class ForgotPasswordView(TemplateView):
    """Forgot password page"""

    template_name = "pages/forgot-password.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Reset Password - Wellness & Rehab Center"
        return context


class ResetPasswordView(TemplateView):
    """Reset password page - for when user clicks link in email"""

    template_name = "pages/reset-password.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Set New Password - Wellness & Rehab Center"
        return context


class LogoutView(View):
    """Logout view"""

    def get(self, request, *args, **kwargs):
        # In a real app, you would handle logout logic here
        return redirect("home")


# Footer Pages
class PrivacyView(TemplateView):
    """Privacy policy page"""

    template_name = "pages/privacy.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Privacy Policy - Wellness & Rehab Center"
        return context


class TermsView(TemplateView):
    """Terms of service page"""

    template_name = "pages/terms.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Terms of Service - Wellness & Rehab Center"
        return context


class SitemapView(TemplateView):
    """Sitemap page"""

    template_name = "pages/sitemap.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Sitemap - Wellness & Rehab Center"
        return context


class InsuranceView(TemplateView):
    """Insurance information page"""

    template_name = "pages/insurance.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Insurance - Wellness & Rehab Center"
        return context


class CareersView(TemplateView):
    """Careers page"""

    template_name = "pages/careers.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Careers - Wellness & Rehab Center"
        return context


# Allsvenskan Football API-Powered Views
class StandingsView(TemplateView):
    """Allsvenskan league table/standings with live API data"""

    template_name = "pages/table.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "ALLSVENSKAN Insikter - Table 2024/25 Standings"

        try:
            # Get league standings from API
            standings = api_football_service.get_standings()
            context["standings"] = standings
            context["standings_available"] = True

            # Get league info
            league_info = api_football_service.get_league_info()
            context["league_info"] = league_info

            # Get additional data for insights section
            try:
                context["top_scorers"] = api_football_service.get_top_scorers(limit=5)
            except Exception as e:
                logger.warning(f"Could not load top scorers: {e}")
                context["top_scorers"] = []

            try:
                context["top_assists"] = api_football_service.get_top_assists(limit=5)
            except Exception as e:
                logger.warning(f"Could not load top assists: {e}")
                context["top_assists"] = []

            try:
                context["clean_sheets"] = api_football_service.get_clean_sheets(limit=5)
            except Exception as e:
                logger.warning(f"Could not load clean sheets: {e}")
                context["clean_sheets"] = []

            # API data availability flag
            context["api_data_available"] = True

            logger.info(f"Successfully loaded standings with {len(standings)} teams")

        except APIFootballError as e:
            logger.error(f"Failed to load standings: {e}")
            messages.error(self.request, _("Unable to load current standings. Please try again later."))
            context["standings"] = []
            context["standings_available"] = False

        except Exception as e:
            logger.error(f"Unexpected error loading standings: {e}")
            messages.error(self.request, _("An unexpected error occurred loading the table."))
            context["standings"] = []
            context["standings_available"] = False

        return context


class FixturesView(TemplateView):
    """Allsvenskan fixtures and results with live API data"""

    template_name = "pages/fixtures.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "ALLSVENSKAN Insikter - Fixtures & Results 2024/25"

        try:
            # Get upcoming fixtures
            upcoming_fixtures = api_football_service.get_fixtures(status='NS', next=10)
            context["upcoming_fixtures"] = upcoming_fixtures

            # Get recent results
            recent_results = api_football_service.get_fixtures(status='FT', last=10)
            context["recent_results"] = recent_results

            # Get live matches if any
            live_matches = api_football_service.get_live_fixtures()
            context["live_matches"] = live_matches

            context["fixtures_available"] = True
            logger.info(f"Loaded {len(upcoming_fixtures)} upcoming fixtures, {len(recent_results)} recent results, {len(live_matches)} live matches")

        except APIFootballError as e:
            logger.error(f"Failed to load fixtures: {e}")
            messages.error(self.request, _("Unable to load fixtures. Please try again later."))
            context["upcoming_fixtures"] = []
            context["recent_results"] = []
            context["live_matches"] = []
            context["fixtures_available"] = False

        except Exception as e:
            logger.error(f"Unexpected error loading fixtures: {e}")
            messages.error(self.request, _("An unexpected error occurred loading fixtures."))
            context["upcoming_fixtures"] = []
            context["recent_results"] = []
            context["live_matches"] = []
            context["fixtures_available"] = False

        return context


class LiveView(TemplateView):
    """Live Allsvenskan matches with auto-refresh"""

    template_name = "pages/live.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "ALLSVENSKAN Insikter - Live Matches"

        try:
            # Get currently live matches
            live_matches = api_football_service.get_live_fixtures()
            context["live_matches"] = live_matches
            context["has_live_matches"] = len(live_matches) > 0

            # Also get today's fixtures for context
            from datetime import datetime
            today = datetime.now().strftime('%Y-%m-%d')
            todays_fixtures = api_football_service.get_fixtures()
            # Filter for today's matches (you might want to adjust this based on API response format)
            context["todays_fixtures"] = todays_fixtures

            logger.info(f"Loaded {len(live_matches)} live matches")

        except APIFootballError as e:
            logger.error(f"Failed to load live matches: {e}")
            messages.error(self.request, _("Unable to load live match data. Please try again later."))
            context["live_matches"] = []
            context["has_live_matches"] = False
            context["todays_fixtures"] = []

        except Exception as e:
            logger.error(f"Unexpected error loading live matches: {e}")
            messages.error(self.request, _("An unexpected error occurred loading live data."))
            context["live_matches"] = []
            context["has_live_matches"] = False
            context["todays_fixtures"] = []

        return context


class TeamsView(TemplateView):
    """Allsvenskan teams with live API data"""

    template_name = "pages/teams.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "ALLSVENSKAN Insikter - Teams, Squads & Stats"

        try:
            # Get all teams
            teams = api_football_service.get_teams()
            context["teams"] = teams

            # Get standings for team positions
            standings = api_football_service.get_standings()
            context["standings"] = standings

            # Create a mapping of team positions for easy lookup
            team_positions = {}
            for position, team_data in enumerate(standings, 1):
                team_id = team_data.get('team', {}).get('id')
                if team_id:
                    team_positions[team_id] = {
                        'position': position,
                        'points': team_data.get('points', 0),
                        'played': team_data.get('all', {}).get('played', 0)
                    }

            context["team_positions"] = team_positions
            context["teams_available"] = True

            logger.info(f"Successfully loaded {len(teams)} teams")

        except APIFootballError as e:
            logger.error(f"Failed to load teams: {e}")
            messages.error(self.request, _("Unable to load team data. Please try again later."))
            context["teams"] = []
            context["standings"] = []
            context["team_positions"] = {}
            context["teams_available"] = False

        except Exception as e:
            logger.error(f"Unexpected error loading teams: {e}")
            messages.error(self.request, _("An unexpected error occurred loading team data."))
            context["teams"] = []
            context["standings"] = []
            context["team_positions"] = {}
            context["teams_available"] = False

        return context


class TopScorersView(TemplateView):
    """Allsvenskan top scorers with live API data"""

    template_name = "pages/players.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "ALLSVENSKAN Insikter - Players, Stats & Top Scorers"

        try:
            # Get top scorers
            top_scorers = api_football_service.get_top_scorers(limit=20)
            context["top_scorers"] = top_scorers

            # You could also add other player statistics here
            # like top assists, most cards, etc. depending on API endpoints

            context["players_available"] = True
            logger.info(f"Successfully loaded {len(top_scorers)} top scorers")

        except APIFootballError as e:
            logger.error(f"Failed to load player data: {e}")
            messages.error(self.request, _("Unable to load player statistics. Please try again later."))
            context["top_scorers"] = []
            context["players_available"] = False

        except Exception as e:
            logger.error(f"Unexpected error loading players: {e}")
            messages.error(self.request, _("An unexpected error occurred loading player data."))
            context["top_scorers"] = []
            context["players_available"] = False

        return context


# Legacy class-based views (keeping for backwards compatibility)
class TableView(StandingsView):
    """Legacy alias for StandingsView"""
    pass


class PlayersView(TemplateView):
    """Allsvenskan players with position filtering"""

    template_name = "pages/players.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "ALLSVENSKAN Insikter - Players"

        # Get filters from request
        position_filter = self.request.GET.get('position', '')
        team_filter = self.request.GET.get('team', '')
        context["selected_position"] = position_filter
        context["selected_team"] = team_filter

        try:
            # Get all players from all teams in the league
            all_players = api_football_service.get_all_league_players()

            # Also get top scorers and assists data to enhance player stats
            try:
                top_scorers = api_football_service.get_top_scorers(limit=50)
                top_assists = api_football_service.get_top_assists(limit=50)

                # Create lookup dictionaries for stats
                scorer_stats = {p.get('player', {}).get('id'): p for p in top_scorers}
                assist_stats = {p.get('player', {}).get('id'): p for p in top_assists}

                # Enhance player stats with top scorer/assist data
                for player in all_players:
                    player_id = player.get('player', {}).get('id')
                    if player_id:
                        # Update with scorer stats if available
                        if player_id in scorer_stats:
                            scorer_data = scorer_stats[player_id]
                            if scorer_data.get('statistics'):
                                player['statistics'] = scorer_data['statistics']

                        # Update with assist stats if available
                        elif player_id in assist_stats:
                            assist_data = assist_stats[player_id]
                            if assist_data.get('statistics'):
                                player['statistics'] = assist_data['statistics']

                logger.info(f"Enhanced {len(all_players)} players with top scorer/assist data")

            except Exception as e:
                logger.warning(f"Could not enhance player data with top stats: {e}")

            if not all_players:
                # Fallback: try to get some data from top scorers/assists only
                logger.warning("No players from get_all_league_players, trying fallback methods")
                top_scorers = api_football_service.get_top_scorers(limit=50)
                top_assists = api_football_service.get_top_assists(limit=50)

                # Combine and deduplicate players
                all_players_dict = {}

                # Add top scorers
                for player in top_scorers:
                    player_id = player.get('player', {}).get('id')
                    if player_id:
                        all_players_dict[player_id] = player

                # Add top assists (merge if already exists)
                for player in top_assists:
                    player_id = player.get('player', {}).get('id')
                    if player_id:
                        if player_id in all_players_dict:
                            # Merge assist data
                            existing = all_players_dict[player_id]
                            existing.setdefault('assists', player.get('statistics', [{}])[0].get('goals', {}).get('assists', 0))
                        else:
                            all_players_dict[player_id] = player

                all_players = list(all_players_dict.values())

            # Apply filters
            filtered_players = all_players

            # Filter by position if specified
            if position_filter:
                temp_filtered = []
                for player in filtered_players:
                    player_position = player.get('statistics', [{}])[0].get('games', {}).get('position', '')
                    if player_position and position_filter.lower() in player_position.lower():
                        temp_filtered.append(player)
                filtered_players = temp_filtered

            # Filter by team if specified
            if team_filter:
                temp_filtered = []
                for player in filtered_players:
                    team_name = player.get('statistics', [{}])[0].get('team', {}).get('name', '')
                    if team_name and team_filter.lower() in team_name.lower():
                        temp_filtered.append(player)
                filtered_players = temp_filtered

            context["players"] = filtered_players

            # Get unique positions for filter options
            positions = set()
            teams = set()
            for player in all_players:
                stats = player.get('statistics', [{}])[0] if player.get('statistics') else {}

                position = stats.get('games', {}).get('position', '')
                if position:
                    positions.add(position)

                team_name = stats.get('team', {}).get('name', '')
                if team_name:
                    teams.add(team_name)

            context["available_positions"] = sorted(list(positions))
            context["available_teams"] = sorted(list(teams))

            context["players_available"] = True
            logger.info(f"Successfully loaded {len(context['players'])} players (filter: {position_filter or 'all'})")

        except APIFootballError as e:
            logger.error(f"Failed to load player data: {e}")
            messages.error(self.request, _("Unable to load player statistics. Please try again later."))
            context["players"] = []
            context["players_available"] = False
            context["available_positions"] = []
            context["available_teams"] = []

        except Exception as e:
            logger.error(f"Unexpected error loading players: {e}")
            messages.error(self.request, _("An unexpected error occurred loading player data."))
            context["players"] = []
            context["players_available"] = False
            context["available_positions"] = []
            context["available_teams"] = []

        return context


class TopScorersView(TemplateView):
    """Dedicated top scorers page"""

    template_name = "pages/top-scorers.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "ALLSVENSKAN Insikter - Top Scorers"

        try:
            # Get top scorers
            top_scorers = api_football_service.get_top_scorers(limit=30)
            context["top_scorers"] = top_scorers
            context["players_available"] = True
            logger.info(f"Successfully loaded {len(top_scorers)} top scorers")

        except APIFootballError as e:
            logger.error(f"Failed to load top scorers: {e}")
            messages.error(self.request, _("Unable to load top scorer statistics. Please try again later."))
            context["top_scorers"] = []
            context["players_available"] = False

        except Exception as e:
            logger.error(f"Unexpected error loading top scorers: {e}")
            messages.error(self.request, _("An unexpected error occurred loading top scorer data."))
            context["top_scorers"] = []
            context["players_available"] = False

        return context


class AssistsLeadersView(TemplateView):
    """Assists leaders page"""

    template_name = "pages/assists.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "ALLSVENSKAN Insikter - Assists Leaders"

        try:
            # Get players and sort by assists
            all_players = api_football_service.get_top_scorers(limit=50)

            # Sort by assists (highest first)
            assists_leaders = []
            for player in all_players:
                assists = player.get('statistics', [{}])[0].get('goals', {}).get('assists', 0)
                if assists and assists > 0:
                    assists_leaders.append(player)

            # Sort by assists count
            assists_leaders.sort(key=lambda x: x.get('statistics', [{}])[0].get('goals', {}).get('assists', 0), reverse=True)

            context["assists_leaders"] = assists_leaders[:25]
            context["players_available"] = True
            logger.info(f"Successfully loaded {len(assists_leaders)} assists leaders")

        except APIFootballError as e:
            logger.error(f"Failed to load assists data: {e}")
            messages.error(self.request, _("Unable to load assists statistics. Please try again later."))
            context["assists_leaders"] = []
            context["players_available"] = False

        except Exception as e:
            logger.error(f"Unexpected error loading assists data: {e}")
            messages.error(self.request, _("An unexpected error occurred loading assists data."))
            context["assists_leaders"] = []
            context["players_available"] = False

        return context


class CleanSheetsView(TemplateView):
    """Clean sheets leaders page (goalkeepers)"""

    template_name = "pages/clean-sheets.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "ALLSVENSKAN Insikter - Clean Sheets"

        try:
            # Get players and filter goalkeepers
            all_players = api_football_service.get_top_scorers(limit=50)

            # Filter goalkeepers and sort by clean sheets or saves
            goalkeepers = []
            for player in all_players:
                position = player.get('statistics', [{}])[0].get('games', {}).get('position', '')
                if position and 'keeper' in position.lower():
                    goalkeepers.append(player)

            context["goalkeepers"] = goalkeepers
            context["players_available"] = True
            logger.info(f"Successfully loaded {len(goalkeepers)} goalkeepers")

        except APIFootballError as e:
            logger.error(f"Failed to load goalkeeper data: {e}")
            messages.error(self.request, _("Unable to load goalkeeper statistics. Please try again later."))
            context["goalkeepers"] = []
            context["players_available"] = False

        except Exception as e:
            logger.error(f"Unexpected error loading goalkeeper data: {e}")
            messages.error(self.request, _("An unexpected error occurred loading goalkeeper data."))
            context["goalkeepers"] = []
            context["players_available"] = False

        return context


class TeamDetailView(TemplateView):
    """Team profile page with detailed statistics"""

    template_name = "pages/team-detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team_slug = kwargs.get('team_slug')

        # Get position filter from URL parameters
        position_filter = self.request.GET.get('position', '').strip()

        try:
            # Get all teams to find the specific team by slug
            teams = api_football_service.get_teams()
            team_data = None
            team_id = None

            for team_info in teams:
                team_name = team_info.get('team', {}).get('name', '')
                # Create slug from team name (lowercase, replace spaces with hyphens)
                team_name_slug = team_name.lower().replace(' ', '-').replace('ö', 'o').replace('ä', 'a').replace('å', 'a')
                if team_name_slug == team_slug:
                    team_data = team_info
                    team_id = team_info.get('team', {}).get('id')
                    break

            if not team_data or not team_id:
                context["team_available"] = False
                context["error_message"] = "Team not found"
                return context

            context["team"] = team_data.get('team')
            context["venue"] = team_data.get('venue')

            # Get detailed venue information if venue ID is available
            venue_basic = team_data.get('venue', {})
            if venue_basic and venue_basic.get('id'):
                try:
                    venue_details = api_football_service.get_venue_details(venue_basic.get('id'))
                    if venue_details:
                        # Merge basic venue info with detailed info
                        context["venue_details"] = venue_details
                    else:
                        context["venue_details"] = venue_basic
                except Exception as e:
                    logger.warning(f"Failed to get detailed venue info: {e}")
                    context["venue_details"] = venue_basic
            else:
                context["venue_details"] = venue_basic

            # Get team statistics
            team_stats = api_football_service.get_team_statistics(team_id)
            context["team_stats"] = team_stats

            # Get team formations
            team_formations = api_football_service.get_team_lineups(team_id)
            context["team_formations"] = team_formations

            # Get team's standings position
            standings = api_football_service.get_standings()
            for position, standing in enumerate(standings, 1):
                if standing.get('team', {}).get('id') == team_id:
                    context["team_standing"] = standing
                    context["league_position"] = position
                    break

            # Get team's recent fixtures
            recent_fixtures = api_football_service.get_fixtures(team_id=team_id, last=5)
            context["recent_fixtures"] = recent_fixtures

            # Get team's upcoming fixtures
            upcoming_fixtures = api_football_service.get_fixtures(team_id=team_id, next=5)
            context["upcoming_fixtures"] = upcoming_fixtures

            # Get all fixtures for the team (for fixtures tab)
            all_fixtures = api_football_service.get_fixtures(team_id=team_id)
            context["all_fixtures"] = all_fixtures

            # Get team squad (all players) using the correct endpoint
            team_squad = api_football_service.get_team_squad(team_id)

            # Process squad data - use squad info directly as it contains position info
            team_players = []
            available_positions = set()

            for squad_player in team_squad:
                # Use squad data directly which contains position information
                position = squad_player.get('position', '')
                if position:
                    available_positions.add(position)

                # Apply position filter if specified
                if not position_filter or (position and position.lower() == position_filter.lower()):
                    # Format player data to match expected structure
                    player_data = {
                        'player': {
                            'id': squad_player.get('id'),
                            'name': squad_player.get('name', 'Unknown'),
                            'age': squad_player.get('age'),
                            'photo': squad_player.get('photo'),
                            'nationality': squad_player.get('nationality')
                        },
                        'statistics': [{
                            'games': {
                                'position': position,
                                'appearences': 0,  # Will be populated if detailed stats are needed
                            },
                            'goals': {'total': 0},
                            'team': {'id': team_id}
                        }]
                    }
                    team_players.append(player_data)

            context["team_players"] = team_players
            context["available_positions"] = sorted(list(available_positions))
            context["current_position_filter"] = position_filter

            # Get team coaching staff
            try:
                team_coaches = api_football_service.get_team_coaches(team_id)
                context["team_coaches"] = team_coaches

                # Get head coach (usually the first one or specifically marked)
                head_coach = None
                for coach in team_coaches:
                    if coach.get('career', []):
                        # Find current role with this team
                        for career_entry in coach['career']:
                            if (career_entry.get('team', {}).get('id') == team_id and
                                career_entry.get('end') is None):  # Current position
                                head_coach = coach
                                break
                        if head_coach:
                            break

                if not head_coach and team_coaches:
                    head_coach = team_coaches[0]  # Fallback to first coach

                context["head_coach"] = head_coach
            except Exception as e:
                logger.warning(f"Failed to get coaching staff: {e}")
                context["team_coaches"] = []
                context["head_coach"] = None

            context["team_available"] = True
            context["page_title"] = f"ALLSVENSKAN Insikter - {context['team'].get('name', 'Team')}"

            logger.info(f"Successfully loaded team profile for ID {team_id}: {context['team'].get('name')} with {len(team_players)} players")

        except APIFootballError as e:
            logger.error(f"Failed to load team data: {e}")
            messages.error(self.request, _("Unable to load team information. Please try again later."))
            context["team_available"] = False
            context["error_message"] = str(e)

        except Exception as e:
            logger.error(f"Unexpected error loading team: {e}")
            messages.error(self.request, _("An unexpected error occurred loading team data."))
            context["team_available"] = False
            context["error_message"] = "Unexpected error"

        return context


# AJAX API Endpoints for live data updates
class LiveDataAPIView(View):
    """AJAX endpoint for live match data updates"""

    def get(self, request, *args, **kwargs):
        """Return live match data as JSON for AJAX updates"""
        try:
            live_matches = api_football_service.get_live_fixtures()

            # Format data for frontend consumption
            formatted_matches = []
            for match in live_matches:
                formatted_match = {
                    'id': match.get('fixture', {}).get('id'),
                    'home_team': match.get('teams', {}).get('home', {}).get('name'),
                    'away_team': match.get('teams', {}).get('away', {}).get('name'),
                    'home_score': match.get('goals', {}).get('home'),
                    'away_score': match.get('goals', {}).get('away'),
                    'status': match.get('fixture', {}).get('status', {}).get('long'),
                    'elapsed': match.get('fixture', {}).get('status', {}).get('elapsed'),
                    'venue': match.get('fixture', {}).get('venue', {}).get('name')
                }
                formatted_matches.append(formatted_match)

            return JsonResponse({
                'success': True,
                'matches': formatted_matches,
                'count': len(formatted_matches)
            })

        except APIFootballError as e:
            logger.error(f"API error in live data endpoint: {e}")
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)

        except Exception as e:
            logger.error(f"Unexpected error in live data endpoint: {e}")
            return JsonResponse({
                'success': False,
                'error': 'An unexpected error occurred'
            }, status=500)


class PlayerDetailView(TemplateView):
    """Individual player profile page with detailed statistics"""

    template_name = "pages/player-detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        player_slug = kwargs.get('player_slug')

        context["page_title"] = "Player Profile - ALLSVENSKAN Insikter"

        try:
            if not player_slug:
                # Player slug not provided
                context["player"] = None
                return context

            # Get all players from all teams in the league (same as PlayersView)
            all_players = api_football_service.get_all_league_players()

            # Find the matching player from the list by comparing slugified names
            matching_player = None
            from django.utils.text import slugify

            for player in all_players:
                player_name = player.get('player', {}).get('name', '')
                if slugify(player_name) == player_slug:
                    matching_player = player
                    break

            if matching_player:
                # This maintains the expected structure: player.player.name, player.statistics.0.goals.total, etc.
                context["player"] = matching_player
                context["player_available"] = True

                # Update page title with player name
                player_name_title = matching_player.get('player', {}).get('name', '')
                if player_name_title:
                    context["page_title"] = f"{player_name_title} - ALLSVENSKAN Insikter"

                logger.info(f"Successfully loaded player profile: {player_name_title} (slug: {player_slug})")

            else:
                context["player"] = None
                logger.warning(f"Player not found for slug: {player_slug}. Searched through {len(all_players)} players.")

        except APIFootballError as e:
            logger.error(f"Failed to load player data: {e}")
            messages.error(self.request, _("Unable to load player profile. Please try again later."))
            context["player"] = None

        except Exception as e:
            logger.error(f"Unexpected error loading player data: {e}")
            messages.error(self.request, _("An unexpected error occurred loading the player profile."))
            context["player"] = None

        return context


class StandingsAPIView(View):
    """AJAX endpoint for standings data updates"""

    def get(self, request, *args, **kwargs):
        """Return standings data as JSON for AJAX updates"""
        try:
            standings = api_football_service.get_standings()

            # Format data for frontend consumption
            formatted_standings = []
            for position, team_data in enumerate(standings, 1):
                formatted_team = {
                    'position': position,
                    'team_name': team_data.get('team', {}).get('name'),
                    'team_logo': team_data.get('team', {}).get('logo'),
                    'played': team_data.get('all', {}).get('played'),
                    'won': team_data.get('all', {}).get('win'),
                    'drawn': team_data.get('all', {}).get('draw'),
                    'lost': team_data.get('all', {}).get('lose'),
                    'goals_for': team_data.get('all', {}).get('goals', {}).get('for'),
                    'goals_against': team_data.get('all', {}).get('goals', {}).get('against'),
                    'goal_difference': team_data.get('goalsDiff'),
                    'points': team_data.get('points'),
                    'form': team_data.get('form')
                }
                formatted_standings.append(formatted_team)

            return JsonResponse({
                'success': True,
                'standings': formatted_standings,
                'count': len(formatted_standings)
            })

        except APIFootballError as e:
            logger.error(f"API error in standings endpoint: {e}")
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)

        except Exception as e:
            logger.error(f"Unexpected error in standings endpoint: {e}")
            return JsonResponse({
                'success': False,
                'error': 'An unexpected error occurred'
            }, status=500)


class ShopView(TemplateView):
    """Premier League shop page"""

    template_name = "pages/shop.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Premier League Shop"
        return context


class BettingView(TemplateView):
    """Premier League betting page"""

    template_name = "pages/betting.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Premier League Betting"
        return context


class SearchAPIView(View):
    """AJAX endpoint for search functionality"""

    def get_products_data(self):
        """Load products from JSON file"""
        try:
            products_path = os.path.join(settings.BASE_DIR, 'static', 'data', 'products.json')
            with open(products_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading products data: {e}")
            return []

    def get(self, request, *args, **kwargs):
        """Search across products, teams, and other content"""
        query = request.GET.get('q', '').strip().lower()

        if not query:
            return JsonResponse({
                'success': True,
                'results': {
                    'products': [],
                    'teams': [],
                    'quick_links': []
                }
            })

        try:
            results = {
                'products': [],
                'teams': [],
                'quick_links': []
            }

            # Search products
            products = self.get_products_data()
            for product in products:
                name = product.get('name', '').lower()
                description = product.get('description', '').lower()
                team = product.get('team', '').lower() if product.get('team') else ''
                category = product.get('category', '').lower()

                if (query in name or
                    query in description or
                    query in team or
                    query in category):
                    results['products'].append({
                        'id': product.get('id'),
                        'name': product.get('name'),
                        'team': product.get('team'),
                        'price': product.get('price'),
                        'image': product.get('image'),
                        'category': product.get('category'),
                        'slug': self.create_slug(product.get('name', ''))
                    })

            # Search teams (Swedish Allsvenskan teams)
            team_matches = []
            teams = [
                'Malmö FF', 'Hammarby FF', 'Djurgården IF', 'AIK Stockholm',
                'IFK Göteborg', 'BK Häcken', 'IF Elfsborg', 'IFK Norrköping',
                'Kalmar FF', 'IK Sirius', 'Degerfors IF', 'Varbergs BoIS',
                'Halmstads BK', 'GIF Sundsvall', 'Örebro SK', 'Mjällby AIF'
            ]

            for team in teams:
                if query in team.lower():
                    team_matches.append({
                        'name': team,
                        'slug': self.create_slug(team),
                        'logo_color': self.get_team_color(team)
                    })

            results['teams'] = team_matches[:5]  # Limit to 5 teams

            # Add quick links based on query
            quick_links = []
            link_mappings = {
                'shop': {'name': 'Shop', 'url': '/shop/'},
                'cart': {'name': 'Shopping Cart', 'url': '/cart/'},
                'fixtures': {'name': 'Fixtures & Results', 'url': '/fixtures/'},
                'table': {'name': 'League Table', 'url': '/table/'},
                'teams': {'name': 'All Teams', 'url': '/teams/'},
                'players': {'name': 'Players', 'url': '/players/'},
                'betting': {'name': 'Betting Tips', 'url': '/betting/'},
                'live': {'name': 'Live Coverage', 'url': '/live/'},
            }

            for key, link_data in link_mappings.items():
                if query in key or query in link_data['name'].lower():
                    quick_links.append(link_data)

            results['quick_links'] = quick_links[:4]  # Limit to 4 links

            return JsonResponse({
                'success': True,
                'results': results,
                'query': query
            })

        except Exception as e:
            logger.error(f"Search error: {e}")
            return JsonResponse({
                'success': False,
                'error': 'Search error occurred'
            }, status=500)

    def create_slug(self, text):
        """Create URL-friendly slug from text"""
        return text.lower().replace(' ', '-').replace('/', '-').replace('&', 'and')

    def get_team_color(self, team):
        """Get team color for display (Swedish Allsvenskan teams)"""
        colors = {
            'Malmö FF': 'bg-sky-400',
            'Hammarby FF': 'bg-green-500',
            'Djurgården IF': 'bg-blue-600',
            'AIK Stockholm': 'bg-gray-800',
            'IFK Göteborg': 'bg-blue-500',
            'BK Häcken': 'bg-yellow-500',
            'IF Elfsborg': 'bg-yellow-600',
            'IFK Norrköping': 'bg-blue-700',
            'Kalmar FF': 'bg-red-500',
            'IK Sirius': 'bg-blue-400',
            'Degerfors IF': 'bg-red-600',
            'Varbergs BoIS': 'bg-green-600',
            'Halmstads BK': 'bg-blue-500',
            'GIF Sundsvall': 'bg-red-500',
            'Örebro SK': 'bg-gray-600',
            'Mjällby AIF': 'bg-yellow-700'
        }
        return colors.get(team, 'bg-blue-500')


# Legal and Information Pages
class AboutView(TemplateView):
    """About page"""
    template_name = "pages/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "About Us - Allsvenskan Insikter"
        return context


class ContactView(TemplateView):
    """Contact page with form handling"""
    template_name = "pages/contact.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Contact Us - Allsvenskan Insikter"
        return context

    def post(self, request, *args, **kwargs):
        """Handle contact form submission"""
        try:
            name = request.POST.get('name', '').strip()
            email = request.POST.get('email', '').strip()
            subject = request.POST.get('subject', '').strip()
            message = request.POST.get('message', '').strip()
            privacy_agreed = request.POST.get('privacy') == 'on'

            # Basic validation
            if not all([name, email, subject, message]) or not privacy_agreed:
                messages.error(request, _('Please fill in all required fields and agree to the privacy policy.'))
                return self.get(request, *args, **kwargs)

            if len(message) < 10:
                messages.error(request, _('Message must be at least 10 characters long.'))
                return self.get(request, *args, **kwargs)

            # Send email (in production, you'd use a proper email service)
            email_subject = f"Contact Form: {subject}"
            email_message = f"""
New contact form submission from {name} ({email}):

Subject: {subject}
Message:
{message}

This message was sent through the contact form on allsvenskaninsikter.se
            """

            try:
                send_mail(
                    email_subject,
                    email_message,
                    settings.DEFAULT_FROM_EMAIL,
                    ['info@allsvenskaninsikter.se'],
                    fail_silently=False,
                )
                messages.success(request, _('Thank you for your message! We will get back to you within 24 hours.'))
            except Exception as e:
                logger.error(f"Failed to send contact email: {e}")
                messages.error(request, _('There was an error sending your message. Please try again or contact us directly.'))

        except Exception as e:
            logger.error(f"Contact form error: {e}")
            messages.error(request, _('An unexpected error occurred. Please try again.'))

        return self.get(request, *args, **kwargs)


class PrivacyPolicyView(TemplateView):
    """Privacy Policy page"""
    template_name = "pages/privacy-policy.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Privacy Policy - Allsvenskan Insikter"
        return context


class TermsOfServiceView(TemplateView):
    """Terms of Service page"""
    template_name = "pages/terms-of-service.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Terms of Service - Allsvenskan Insikter"
        return context


class CookiePolicyView(TemplateView):
    """Cookie Policy page"""
    template_name = "pages/cookie-policy.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Cookie Policy - Allsvenskan Insikter"
        return context


class AccessibilityView(TemplateView):
    """Accessibility Statement page"""
    template_name = "pages/accessibility.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Accessibility Statement - Allsvenskan Insikter"
        return context
