#!/usr/bin/env python
"""
Quick API test script for Django environment.
"""

# Test imports
try:
    from apps.core.services.api_football import api_football_service, APIFootballError
    print("✅ API service imported successfully")
except ImportError as e:
    print(f"❌ Failed to import API service: {e}")
    exit(1)

# Test configuration
try:
    if hasattr(api_football_service, 'api_key') and api_football_service.api_key:
        print("✅ API key is configured")
        print(f"   League ID: {api_football_service.league_id}")
        print(f"   API Host: {api_football_service.api_host}")
    else:
        print("❌ API key not configured")
        exit(1)
except Exception as e:
    print(f"❌ Configuration error: {e}")
    exit(1)

# Test API endpoints
print("\n=== Testing API Endpoints ===")

# Test league info
print("\n1. Testing League Info...")
try:
    league_info = api_football_service.get_league_info()
    if league_info:
        league_name = league_info.get('league', {}).get('name', 'Unknown')
        country = league_info.get('country', {}).get('name', 'Unknown')
        print(f"✅ League: {league_name} ({country})")
    else:
        print("⚠️  No league info returned")
except Exception as e:
    print(f"❌ League info failed: {e}")

# Test standings
print("\n2. Testing Standings...")
try:
    standings = api_football_service.get_standings()
    if standings and len(standings) > 0:
        print(f"✅ Retrieved {len(standings)} teams in standings")

        # Show top 3 teams
        for i, team_data in enumerate(standings[:3], 1):
            team_name = team_data.get('team', {}).get('name', 'Unknown')
            points = team_data.get('points', 0)
            played = team_data.get('all', {}).get('played', 0)
            print(f"   {i}. {team_name} - {points} pts ({played} played)")
    else:
        print("⚠️  No standings returned")
except Exception as e:
    print(f"❌ Standings failed: {e}")

# Test teams
print("\n3. Testing Teams...")
try:
    teams = api_football_service.get_teams()
    if teams and len(teams) > 0:
        print(f"✅ Retrieved {len(teams)} teams")

        # Show first 3 teams
        for team in teams[:3]:
            team_name = team.get('team', {}).get('name', 'Unknown')
            venue = team.get('venue', {}).get('name', 'Unknown')
            print(f"   - {team_name} (Home: {venue})")
    else:
        print("⚠️  No teams returned")
except Exception as e:
    print(f"❌ Teams failed: {e}")

# Test fixtures
print("\n4. Testing Recent Fixtures...")
try:
    fixtures = api_football_service.get_fixtures(last=3)
    if fixtures and len(fixtures) > 0:
        print(f"✅ Retrieved {len(fixtures)} recent fixtures")

        for fixture in fixtures[:3]:
            home_team = fixture.get('teams', {}).get('home', {}).get('name', 'Unknown')
            away_team = fixture.get('teams', {}).get('away', {}).get('name', 'Unknown')
            home_score = fixture.get('goals', {}).get('home', 0)
            away_score = fixture.get('goals', {}).get('away', 0)
            status = fixture.get('fixture', {}).get('status', {}).get('short', 'Unknown')
            print(f"   {home_team} {home_score}-{away_score} {away_team} ({status})")
    else:
        print("⚠️  No fixtures returned")
except Exception as e:
    print(f"❌ Fixtures failed: {e}")

# Test top scorers
print("\n5. Testing Top Scorers...")
try:
    scorers = api_football_service.get_top_scorers(limit=5)
    if scorers and len(scorers) > 0:
        print(f"✅ Retrieved {len(scorers)} top scorers")

        for i, scorer in enumerate(scorers[:5], 1):
            player_name = scorer.get('player', {}).get('name', 'Unknown')
            team_name = scorer.get('statistics', [{}])[0].get('team', {}).get('name', 'Unknown') if scorer.get('statistics') else 'Unknown'
            goals = scorer.get('statistics', [{}])[0].get('goals', {}).get('total', 0) if scorer.get('statistics') else 0
            print(f"   {i}. {player_name} ({team_name}) - {goals} goals")
    else:
        print("⚠️  No top scorers returned")
except Exception as e:
    print(f"❌ Top scorers failed: {e}")

print("\n=== API Test Complete ===")
print("✅ If you see data above, the API integration is working!")
print("\nYou can now:")
print("1. Start the development server: python manage.py runserver")
print("2. Visit the pages to see live data:")
print("   - http://localhost:8000/ (Home page)")
print("   - http://localhost:8000/table/ (League table)")
print("   - http://localhost:8000/fixtures/ (Fixtures)")
print("   - http://localhost:8000/teams/ (Teams)")
print("   - http://localhost:8000/players/ (Top scorers)")
print("   - http://localhost:8000/live/ (Live matches)")