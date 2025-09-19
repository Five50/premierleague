from django import template
from django.urls import reverse
from django.utils.translation import get_language

register = template.Library()


@register.simple_tag
def trans_url(url_name, lang_code=None):
    """Generate URL for specific language."""
    if lang_code == "en" and not url_name.endswith("-en"):
        # Try English version of URL
        try:
            return reverse(f"{url_name}-en")
        except Exception:
            pass
    return reverse(url_name)


@register.simple_tag
def get_translated_content(content_dict, field_name):
    """Get content in current language with fallback."""
    current_lang = get_language()

    # Try current language
    if isinstance(content_dict, dict):
        if current_lang in content_dict:
            return content_dict[current_lang].get(field_name, "")
        # Fallback to Swedish
        if "sv" in content_dict:
            return content_dict["sv"].get(field_name, "")

    return content_dict if isinstance(content_dict, str) else ""


@register.filter
def translate_menu_item(text, lang=None):
    """Translate menu items."""
    if lang is None:
        lang = get_language()

    translations = {
        "en": {
            "Lån": "Loans",
            "Sparande": "Savings",
            "Kreditkort": "Credit Cards",
            "Företagslån": "Business Loans",
            "Blogg": "Blog",
            "Privatlån": "Personal Loans",
            "Billån": "Car Loans",
            "Samlingslån": "Debt Consolidation",
            "Sparkonto": "Savings Account",
            "Fondrobot": "Robo-Advisor",
            "Aktier": "Stocks",
        },
        "sv": {
            "Loans": "Lån",
            "Savings": "Sparande",
            "Credit Cards": "Kreditkort",
            "Business Loans": "Företagslån",
            "Blog": "Blogg",
            "Personal Loans": "Privatlån",
            "Car Loans": "Billån",
            "Debt Consolidation": "Samlingslån",
            "Savings Account": "Sparkonto",
            "Robo-Advisor": "Fondrobot",
            "Stocks": "Aktier",
        },
    }

    if lang in translations and text in translations[lang]:
        return translations[lang][text]

    return text


@register.simple_tag
def switch_language_url(request, lang_code):
    """Generate URL for switching language."""
    path = request.get_full_path()

    # Remove language prefix if exists
    if path.startswith("/en/"):
        path = path[3:]
    elif path.startswith("/sv/"):
        path = path[3:]

    # Add new language prefix for English
    if lang_code == "en":
        return f"/en{path}"

    # Swedish doesn't need prefix
    return path


@register.filter
def team_slug(team_name):
    """Convert team name to URL slug."""
    if not team_name:
        return ""
    # Lowercase and replace spaces with hyphens, handle Swedish characters
    return (team_name.lower()
            .replace(' ', '-')
            .replace('ö', 'o')
            .replace('ä', 'a')
            .replace('å', 'a')
            .replace('ü', 'u')
            .replace('é', 'e'))
