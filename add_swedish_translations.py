#!/usr/bin/env python3

import re
import sys

# Swedish translations for key Premier League terms
TRANSLATIONS = {
    # Core Terms
    "Teams": "Lag",
    "Players": "Spelare", 
    "Fixtures": "Matcher",
    "Shop": "Butik",
    "League Table": "Tabell",
    "Premier League Table": "Premier League Tabell",
    "Position": "Position",
    "Points": "Poäng",
    "Matches": "Matcher",
    "Goals": "Mål",
    
    # Pages and Sections
    "Premier League Hub": "Premier League Hub",
    "Premier League Teams": "Premier League Lag",
    "Premier League Players": "Premier League Spelare",
    "Premier League Shop": "Premier League Butik",
    "Betting Tips & Odds": "Speltips & Odds",
    "Premier League Betting Tips & Odds": "Premier League Speltips & Odds",
    "Fixtures & Results": "Matcher & Resultat",
    
    # Actions
    "View All Teams": "Visa Alla Lag",
    "View All Fixtures": "Visa Alla Matcher",
    "View All Players": "Visa Alla Spelare",
    "Browse Players": "Bläddra Spelare",
    "Continue Shopping": "Fortsätt Handla",
    "Add to Cart": "Lägg i Varukorg",
    "Shopping Cart": "Varukorg",
    "Back to Shop": "Tillbaka till Butik",
    
    # Table Terms
    "W": "V",  # Wins = Vinster
    "D": "O",  # Draws = Oavgjorda  
    "L": "F",  # Losses = Förluster
    "P": "M",  # Played = Matcher
    "Pts": "P", # Points = Poäng
    
    # Betting Terms
    "Place Bet": "Placera Bet",
    "View Full Analysis": "Visa Full Analys",
    "Expert Betting Tips": "Expert Speltips",
    "Match Result": "Matchresultat",
    "odds": "odds",
    "confidence": "förtroende",
    
    # Shopping Terms
    "Price": "Pris",
    "Size": "Storlek",
    "All Teams": "Alla Lag",
    "Featured": "Utvalda",
    "Newest First": "Nyaste Först",
    "Price: Low to High": "Pris: Låg till Hög",
    "Price: High to Low": "Pris: Hög till Låg",
    "Name A-Z": "Namn A-Ö",
    
    # Common Terms
    "Home": "Hem",
    "Search": "Sök",
    "Filter": "Filter",
    "Loading": "Laddar",
    "Error": "Fel",
    "Founded": "Grundat",
    "Manager": "Manager",
    "Stadium": "Stadium",
    
    # Messages
    "Loading teams...": "Laddar lag...",
    "Loading players...": "Laddar spelare...",
    "Loading fixtures...": "Laddar matcher...",
    "Loading products...": "Laddar produkter...",
    "No players found": "Inga spelare hittades",
    "Error loading teams data": "Fel vid laddning av lagdata",
    "Error loading players data": "Fel vid laddning av spelardata",
    "Error loading fixtures data": "Fel vid laddning av matchdata",
}

def update_translation_file(filepath):
    """Update the Swedish translation file with our translations"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update each translation
    for english, swedish in TRANSLATIONS.items():
        # Pattern to match msgid "English" followed by empty msgstr ""
        pattern = rf'(msgid "{re.escape(english)}"\nmsgstr ")("")'
        replacement = rf'\1{swedish}\2'
        content = re.sub(pattern, replacement, content)
    
    # Write back the updated content
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Updated {len(TRANSLATIONS)} translations in {filepath}")

if __name__ == "__main__":
    filepath = "locale/sv/LC_MESSAGES/django.po"
    update_translation_file(filepath)