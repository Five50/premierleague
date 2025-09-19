#!/usr/bin/env python
"""
Test script for API Football integration.

This script tests the API service without requiring a full Django setup.
Run this to verify your API key and service configuration.

Usage:
    python test_api_integration.py
"""

import os
import sys
from decouple import Config, RepositoryEnv

# Load environment variables
config = Config(RepositoryEnv('.env'))

# Add apps to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'apps'))

def test_api_configuration():
    """Test basic API configuration."""
    print("=== Testing API Configuration ===")

    api_key = config('RAPIDAPI_KEY', default='')
    api_host = config('RAPIDAPI_HOST', default='v3.football.api-sports.io')
    league_id = config('ALLSVENSKAN_LEAGUE_ID', default=113, cast=int)

    print(f"API Key configured: {'✓' if api_key else '✗'}")
    print(f"API Host: {api_host}")
    print(f"League ID: {league_id}")

    if not api_key:
        print("\n❌ ERROR: RAPIDAPI_KEY not configured!")
        print("Please add your API key to the .env file:")
        print("RAPIDAPI_KEY=your-actual-api-key")
        return False

    return True


def test_api_service():
    """Test API service functionality."""
    print("\n=== Testing API Service ===")

    try:
        # Import our service
        from core.services.api_football import api_football_service, APIFootballError

        print("✓ API service imported successfully")

        # Test league info
        print("\n--- Testing League Info ---")
        try:
            league_info = api_football_service.get_league_info()
            if league_info:
                print(f"✓ League info retrieved: {league_info.get('league', {}).get('name', 'Unknown')}")
                print(f"  Season: {league_info.get('seasons', [{}])[-1].get('year', 'Unknown')}")
            else:
                print("⚠ No league info returned (might be normal if API limits exceeded)")
        except APIFootballError as e:
            print(f"✗ League info failed: {e}")
        except Exception as e:
            print(f"✗ Unexpected error: {e}")

        # Test standings
        print("\n--- Testing Standings ---")
        try:
            standings = api_football_service.get_standings()
            if standings:
                print(f"✓ Standings retrieved: {len(standings)} teams")
                if len(standings) > 0:
                    leader = standings[0]
                    team_name = leader.get('team', {}).get('name', 'Unknown')
                    points = leader.get('points', 0)
                    print(f"  League leader: {team_name} ({points} points)")
            else:
                print("⚠ No standings returned")
        except APIFootballError as e:
            print(f"✗ Standings failed: {e}")
        except Exception as e:
            print(f"✗ Unexpected error: {e}")

        # Test teams
        print("\n--- Testing Teams ---")
        try:
            teams = api_football_service.get_teams()
            if teams:
                print(f"✓ Teams retrieved: {len(teams)} teams")
                if len(teams) > 0:
                    first_team = teams[0]
                    team_name = first_team.get('team', {}).get('name', 'Unknown')
                    venue = first_team.get('venue', {}).get('name', 'Unknown')
                    print(f"  Example team: {team_name} (Home: {venue})")
            else:
                print("⚠ No teams returned")
        except APIFootballError as e:
            print(f"✗ Teams failed: {e}")
        except Exception as e:
            print(f"✗ Unexpected error: {e}")

        # Test fixtures
        print("\n--- Testing Fixtures ---")
        try:
            fixtures = api_football_service.get_fixtures(last=5)
            if fixtures:
                print(f"✓ Fixtures retrieved: {len(fixtures)} recent matches")
                if len(fixtures) > 0:
                    latest = fixtures[0]
                    home_team = latest.get('teams', {}).get('home', {}).get('name', 'Unknown')
                    away_team = latest.get('teams', {}).get('away', {}).get('name', 'Unknown')
                    print(f"  Latest match: {home_team} vs {away_team}")
            else:
                print("⚠ No fixtures returned")
        except APIFootballError as e:
            print(f"✗ Fixtures failed: {e}")
        except Exception as e:
            print(f"✗ Unexpected error: {e}")

        # Test top scorers
        print("\n--- Testing Top Scorers ---")
        try:
            scorers = api_football_service.get_top_scorers(limit=5)
            if scorers:
                print(f"✓ Top scorers retrieved: {len(scorers)} players")
                if len(scorers) > 0:
                    top_scorer = scorers[0]
                    player_name = top_scorer.get('player', {}).get('name', 'Unknown')
                    goals = top_scorer.get('statistics', [{}])[0].get('goals', {}).get('total', 0) if top_scorer.get('statistics') else 0
                    print(f"  Top scorer: {player_name} ({goals} goals)")
            else:
                print("⚠ No top scorers returned")
        except APIFootballError as e:
            print(f"✗ Top scorers failed: {e}")
        except Exception as e:
            print(f"✗ Unexpected error: {e}")

        return True

    except ImportError as e:
        print(f"✗ Failed to import API service: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False


def main():
    """Main test function."""
    print("🚀 ALLSVENSKAN Insikter - API Football Integration Test")
    print("=" * 60)

    # Test configuration
    if not test_api_configuration():
        print("\n❌ Configuration test failed!")
        return 1

    # Test API service
    if not test_api_service():
        print("\n❌ API service test failed!")
        return 1

    print("\n" + "=" * 60)
    print("✅ All tests completed!")
    print("\nNext steps:")
    print("1. Start the Django development server: python manage.py runserver")
    print("2. Visit the Allsvenskan pages to see live data:")
    print("   - http://localhost:8000/table/")
    print("   - http://localhost:8000/fixtures/")
    print("   - http://localhost:8000/teams/")
    print("   - http://localhost:8000/players/")
    print("   - http://localhost:8000/live/")

    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)