"""
API Football Service for Allsvenskan data integration.

This service handles all communication with the API-Football service
(https://rapidapi.com/api-sports/api/api-football) to fetch Allsvenskan
league data including standings, fixtures, teams, and player statistics.
"""

import logging
import requests
from typing import Dict, List, Optional, Any
from django.conf import settings
from django.core.cache import cache
from decouple import config

logger = logging.getLogger(__name__)


class APIFootballError(Exception):
    """Custom exception for API Football service errors."""
    pass


class APIFootballService:
    """
    Service class for interacting with the API Football API.

    Handles authentication, rate limiting, caching, and error handling
    for all Allsvenskan data requests.
    """

    def __init__(self):
        self.base_url = "https://v3.football.api-sports.io"
        # Try multiple possible environment variable names for flexibility
        self.api_key = (
            config('API_FOOTBALL_KEY', default='') or
            config('RAPIDAPI_KEY', default='')
        )
        self.api_host = (
            config('API_FOOTBALL_HOST', default='') or
            config('RAPIDAPI_HOST', default='v3.football.api-sports.io')
        )
        self.league_id = (
            config('SWEDISH_LEAGUE_ID', default=113, cast=int) or
            config('ALLSVENSKAN_LEAGUE_ID', default=113, cast=int)
        )
        self.current_season = 2025

        if not self.api_key:
            logger.warning("API_FOOTBALL_KEY or RAPIDAPI_KEY not configured. API requests will fail.")

    def _get_headers(self) -> Dict[str, str]:
        """Get required headers for API requests."""
        return {
            'X-RapidAPI-Key': self.api_key,
            'X-RapidAPI-Host': self.api_host,
            'Content-Type': 'application/json'
        }

    def _make_request(self, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Make a request to the API Football service.

        Args:
            endpoint: API endpoint path
            params: Query parameters

        Returns:
            Parsed JSON response

        Raises:
            APIFootballError: If request fails or returns error
        """
        if not self.api_key:
            raise APIFootballError("API key not configured")

        url = f"{self.base_url}/{endpoint}"
        headers = self._get_headers()

        # Create cache key from endpoint and params
        cache_key = f"api_football_{endpoint}_{hash(str(sorted((params or {}).items())))}"

        # Try to get from cache first (5 minute cache for most data)
        cached_data = cache.get(cache_key)
        if cached_data:
            logger.debug(f"Cache hit for {endpoint}")
            return cached_data

        try:
            logger.info(f"Making API request to {endpoint} with params: {params}")
            response = requests.get(url, headers=headers, params=params, timeout=30)
            response.raise_for_status()

            data = response.json()

            # Check API response status
            if not data.get('response'):
                error_msg = data.get('errors', {})
                logger.error(f"API returned no data: {error_msg}")
                raise APIFootballError(f"No data returned from API: {error_msg}")

            # Cache successful responses
            cache_timeout = 300 if 'live' in endpoint else 1800  # 5 min for live, 30 min for others
            cache.set(cache_key, data, cache_timeout)

            logger.info(f"Successfully fetched data from {endpoint}")
            return data

        except requests.exceptions.Timeout:
            logger.error(f"Request timeout for {endpoint}")
            raise APIFootballError("Request timeout")
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed for {endpoint}: {str(e)}")
            raise APIFootballError(f"Request failed: {str(e)}")
        except ValueError as e:
            logger.error(f"Invalid JSON response for {endpoint}: {str(e)}")
            raise APIFootballError("Invalid response format")

    def get_league_info(self, season: int = None) -> Dict[str, Any]:
        """
        Get Allsvenskan league information.

        Args:
            season: Season year (defaults to current season)

        Returns:
            League information including format, dates, coverage
        """
        season = season or self.current_season
        params = {
            'id': self.league_id,
            'season': season
        }

        try:
            data = self._make_request('leagues', params)
            if data['response']:
                return data['response'][0]
            return {}
        except APIFootballError as e:
            logger.error(f"Failed to get league info: {e}")
            return {}

    def get_standings(self, season: int = None) -> List[Dict[str, Any]]:
        """
        Get current Allsvenskan league table/standings.

        Args:
            season: Season year (defaults to current season)

        Returns:
            List of team standings with position, points, stats
        """
        season = season or self.current_season
        params = {
            'league': self.league_id,
            'season': season
        }

        try:
            data = self._make_request('standings', params)
            if data['response'] and data['response'][0]['league']['standings']:
                return data['response'][0]['league']['standings'][0]
            return []
        except APIFootballError as e:
            logger.error(f"Failed to get standings: {e}")
            return []

    def get_fixtures(self, season: int = None, status: str = None,
                    team_id: int = None, last: int = None, next: int = None) -> List[Dict[str, Any]]:
        """
        Get Allsvenskan fixtures and results.

        Args:
            season: Season year (defaults to current season)
            status: Filter by match status (NS, LIVE, FT, etc.)
            team_id: Filter by specific team
            last: Get last N matches
            next: Get next N matches

        Returns:
            List of fixtures with match details
        """
        season = season or self.current_season
        params = {
            'league': self.league_id,
            'season': season
        }

        if status:
            params['status'] = status
        if team_id:
            params['team'] = team_id
        if last:
            params['last'] = last
        if next:
            params['next'] = next

        try:
            data = self._make_request('fixtures', params)
            return data['response'] if data['response'] else []
        except APIFootballError as e:
            logger.error(f"Failed to get fixtures: {e}")
            return []

    def get_live_fixtures(self) -> List[Dict[str, Any]]:
        """
        Get currently live Allsvenskan matches.

        Returns:
            List of live matches with real-time data
        """
        params = {
            'league': self.league_id,
            'live': 'all'
        }

        try:
            data = self._make_request('fixtures', params)
            return data['response'] if data['response'] else []
        except APIFootballError as e:
            logger.error(f"Failed to get live fixtures: {e}")
            return []

    def get_teams(self, season: int = None) -> List[Dict[str, Any]]:
        """
        Get all Allsvenskan teams for the season.

        Args:
            season: Season year (defaults to current season)

        Returns:
            List of teams with details, statistics
        """
        season = season or self.current_season
        params = {
            'league': self.league_id,
            'season': season
        }

        try:
            data = self._make_request('teams', params)
            return data['response'] if data['response'] else []
        except APIFootballError as e:
            logger.error(f"Failed to get teams: {e}")
            return []

    def get_top_scorers(self, season: int = None, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Get top goalscorers in Allsvenskan.

        Args:
            season: Season year (defaults to current season)
            limit: Maximum number of players to return

        Returns:
            List of top scorers with goals, team info
        """
        season = season or self.current_season
        params = {
            'league': self.league_id,
            'season': season
        }

        try:
            data = self._make_request('players/topscorers', params)
            scorers = data['response'] if data['response'] else []
            return scorers[:limit]
        except APIFootballError as e:
            logger.error(f"Failed to get top scorers: {e}")
            return []

    def get_top_assists(self, season: int = None, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Get top assist providers in Allsvenskan.

        Args:
            season: Season year (defaults to current season)
            limit: Maximum number of players to return

        Returns:
            List of top assist providers with assists, team info
        """
        season = season or self.current_season
        params = {
            'league': self.league_id,
            'season': season
        }

        try:
            data = self._make_request('players/topassists', params)
            assists = data['response'] if data['response'] else []
            return assists[:limit]
        except APIFootballError as e:
            logger.error(f"Failed to get top assists: {e}")
            return []

    def get_team_statistics(self, team_id: int, season: int = None) -> Dict[str, Any]:
        """
        Get detailed statistics for a specific team.

        Args:
            team_id: Team ID
            season: Season year (defaults to current season)

        Returns:
            Team statistics including goals, cards, performance
        """
        season = season or self.current_season
        params = {
            'league': self.league_id,
            'season': season,
            'team': team_id
        }

        try:
            data = self._make_request('teams/statistics', params)
            if data['response']:
                return data['response']
            return {}
        except APIFootballError as e:
            logger.error(f"Failed to get team statistics: {e}")
            return {}

    def get_team_lineups(self, team_id: int, season: int = None) -> List[Dict[str, Any]]:
        """
        Get most used lineups/formations for a specific team.

        Args:
            team_id: Team ID
            season: Season year (defaults to current season)

        Returns:
            List of team lineups with formation usage statistics
        """
        season = season or self.current_season

        # Get recent fixtures to analyze formations
        fixtures = self.get_fixtures(team_id=team_id, season=season)
        formations = {}

        for fixture in fixtures:
            try:
                # Get detailed fixture data with lineups
                fixture_id = fixture.get('fixture', {}).get('id')
                if fixture_id:
                    lineup_data = self._get_fixture_lineups(fixture_id, team_id)
                    if lineup_data:
                        formation = lineup_data.get('formation')
                        if formation:
                            formations[formation] = formations.get(formation, 0) + 1
            except Exception as e:
                logger.debug(f"Failed to get lineup for fixture {fixture_id}: {e}")
                continue

        # Convert to sorted list
        formation_list = []
        for formation, count in sorted(formations.items(), key=lambda x: x[1], reverse=True):
            formation_list.append({
                'formation': formation,
                'played': count
            })

        return formation_list

    def _get_fixture_lineups(self, fixture_id: int, team_id: int = None) -> Dict[str, Any]:
        """
        Get lineups for a specific fixture.

        Args:
            fixture_id: Fixture ID
            team_id: Optional team ID to filter lineup

        Returns:
            Lineup data for the team
        """
        params = {
            'fixture': fixture_id
        }

        try:
            data = self._make_request('fixtures/lineups', params)
            if data['response']:
                if team_id:
                    # Find lineup for specific team
                    for lineup in data['response']:
                        if lineup.get('team', {}).get('id') == team_id:
                            return lineup
                else:
                    return data['response'][0] if data['response'] else {}
            return {}
        except APIFootballError as e:
            logger.debug(f"Failed to get fixture lineups: {e}")
            return {}

    def get_h2h_matches(self, team1_id: int, team2_id: int, last: int = 10) -> List[Dict[str, Any]]:
        """
        Get head-to-head matches between two teams.

        Args:
            team1_id: First team ID
            team2_id: Second team ID
            last: Number of recent matches to get

        Returns:
            List of head-to-head matches
        """
        params = {
            'h2h': f"{team1_id}-{team2_id}",
            'last': last
        }

        try:
            data = self._make_request('fixtures/headtohead', params)
            return data['response'] if data['response'] else []
        except APIFootballError as e:
            logger.error(f"Failed to get H2H matches: {e}")
            return []

    def get_player_statistics(self, player_id: int, season: int = None) -> Dict[str, Any]:
        """
        Get detailed statistics for a specific player.

        Args:
            player_id: Player ID
            season: Season year (defaults to current season)

        Returns:
            Player statistics including goals, assists, appearances, etc.
        """
        season = season or self.current_season
        params = {
            'id': player_id,
            'season': season
        }

        try:
            data = self._make_request('players', params)
            if data['response'] and len(data['response']) > 0:
                return data['response'][0]
            return {}
        except APIFootballError as e:
            logger.error(f"Failed to get player statistics: {e}")
            return {}

    def get_player_transfers(self, player_id: int) -> List[Dict[str, Any]]:
        """
        Get transfer history for a specific player.

        Args:
            player_id: Player ID

        Returns:
            List of player transfers
        """
        params = {
            'player': player_id
        }

        try:
            data = self._make_request('transfers', params)
            return data['response'] if data['response'] else []
        except APIFootballError as e:
            logger.error(f"Failed to get player transfers: {e}")
            return []

    def get_team_squad(self, team_id: int, season: int = None) -> List[Dict[str, Any]]:
        """
        Get all squad players for a specific team using the correct squads endpoint.

        Args:
            team_id: Team ID to get squad for
            season: Season year (defaults to current season)

        Returns:
            List of all team squad players
        """
        season = season or self.current_season
        params = {
            'team': team_id
        }

        try:
            data = self._make_request('players/squads', params)
            if data['response'] and len(data['response']) > 0:
                return data['response'][0].get('players', [])
            return []
        except APIFootballError as e:
            logger.error(f"Failed to get team squad: {e}")
            return []

    def get_all_league_players(self, season: int = None) -> List[Dict[str, Any]]:
        """
        Get all players from all teams in the Allsvenskan league.

        This method fetches all teams first, then gets the squad for each team,
        and combines player data with their statistics.

        Args:
            season: Season year (defaults to current season)

        Returns:
            List of all players with their team and statistical information
        """
        season = season or self.current_season
        all_players = []

        try:
            # First get all teams in the league
            teams = self.get_teams(season)
            logger.info(f"Found {len(teams)} teams in Allsvenskan")

            for team_data in teams:
                team_info = team_data.get('team', {})
                team_id = team_info.get('id')

                if not team_id:
                    continue

                try:
                    # Get squad for this team
                    squad_players = self.get_team_squad(team_id, season)
                    logger.info(f"Found {len(squad_players)} players for {team_info.get('name')}")

                    # For each player, get their statistics and format the data
                    for player in squad_players:
                        player_id = player.get('id')
                        if not player_id:
                            continue

                        # For efficiency, we'll add players with basic info and get stats later if needed
                        # This reduces the number of API calls significantly
                        formatted_player = {
                            'player': {
                                'id': player.get('id'),
                                'name': player.get('name'),
                                'firstname': player.get('firstname'),
                                'lastname': player.get('lastname'),
                                'age': player.get('age'),
                                'birth': player.get('birth', {}),
                                'nationality': player.get('nationality'),
                                'height': player.get('height'),
                                'weight': player.get('weight'),
                                'photo': player.get('photo')
                            },
                            'statistics': [{
                                'team': team_info,
                                'league': {'id': self.league_id, 'name': 'Allsvenskan'},
                                'games': {'position': player.get('position')},
                                'goals': {'total': 0, 'assists': 0},
                                'cards': {'yellow': 0, 'red': 0}
                            }]
                        }
                        all_players.append(formatted_player)

                except Exception as e:
                    logger.warning(f"Failed to get squad for team {team_info.get('name', 'Unknown')}: {e}")
                    continue

            logger.info(f"Successfully collected {len(all_players)} total players from all teams")
            return all_players

        except APIFootballError as e:
            logger.error(f"Failed to get all league players: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error getting all league players: {e}")
            return []

    def get_team_coaches(self, team_id: int, season: int = None) -> List[Dict[str, Any]]:
        """
        Get coaching staff for a specific team.

        Args:
            team_id: Team ID to get coaches for
            season: Season year (defaults to current season)

        Returns:
            List of team coaches with their information
        """
        season = season or self.current_season
        params = {
            'team': team_id,
            'season': season
        }

        try:
            data = self._make_request('coachs', params)
            return data['response'] if data['response'] else []
        except APIFootballError as e:
            logger.error(f"Failed to get team coaches: {e}")
            return []

    def get_coach_details(self, coach_id: int) -> Dict[str, Any]:
        """
        Get detailed information for a specific coach.

        Args:
            coach_id: Coach ID to get details for

        Returns:
            Detailed coach information
        """
        params = {
            'id': coach_id
        }

        try:
            data = self._make_request('coachs', params)
            if data['response'] and len(data['response']) > 0:
                return data['response'][0]
            return {}
        except APIFootballError as e:
            logger.error(f"Failed to get coach details: {e}")
            return {}

    def get_venue_details(self, venue_id: int) -> Dict[str, Any]:
        """
        Get detailed venue information by venue ID.

        Args:
            venue_id: Venue ID to get details for

        Returns:
            Detailed venue information including capacity, surface, etc.
        """
        params = {
            'id': venue_id
        }

        try:
            data = self._make_request('venues', params)
            if data['response'] and len(data['response']) > 0:
                return data['response'][0]
            return {}
        except APIFootballError as e:
            logger.error(f"Failed to get venue details: {e}")
            return {}

    def search_venues(self, name: str = None, city: str = None, country: str = None) -> List[Dict[str, Any]]:
        """
        Search for venues by name, city, or country.

        Args:
            name: Venue name to search for
            city: City to filter by
            country: Country to filter by

        Returns:
            List of matching venues
        """
        params = {}
        if name:
            params['search'] = name
        if city:
            params['city'] = city
        if country:
            params['country'] = country

        try:
            data = self._make_request('venues', params)
            return data['response'] if data['response'] else []
        except APIFootballError as e:
            logger.error(f"Failed to search venues: {e}")
            return []

    def search_players(self, name: str, league_id: int = None, season: int = None) -> List[Dict[str, Any]]:
        """
        Search for players by name.

        Args:
            name: Player name to search for
            league_id: League ID to filter by (defaults to Allsvenskan)
            season: Season year (defaults to current season)

        Returns:
            List of matching players
        """
        season = season or self.current_season
        league_id = league_id or self.league_id

        params = {
            'search': name,
            'league': league_id,
            'season': season
        }

        try:
            data = self._make_request('players', params)
            return data['response'] if data['response'] else []
        except APIFootballError as e:
            logger.error(f"Failed to search players: {e}")
            return []


# Singleton instance
api_football_service = APIFootballService()