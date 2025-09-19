from django.urls import reverse
from django.utils.translation import get_language


def get_translated_url(url_name, *args, **kwargs):
    """Get URL with current language prefix."""
    return reverse(url_name, args=args, kwargs=kwargs)


def get_content_by_language(content_dict, field_name, default_lang="sv"):
    """Get content based on current language with fallback."""
    current_lang = get_language()

    # Try current language
    if current_lang in content_dict:
        return content_dict[current_lang].get(field_name, "")

    # Fallback to default language
    if default_lang in content_dict:
        return content_dict[default_lang].get(field_name, "")

    return ""


# Translation mappings for URLs
URL_TRANSLATIONS = {
    "sv": {
        "loans": "lan",
        "savings": "spara-pengar",
        "best-interest-rate": "basta-sparrantan",
        "credit-cards": "kreditkort",
        "no-annual-fee": "utan-arsavgift",
        "business-loans": "foretagslan",
        "unsecured": "utan-sakerhet",
        "blog": "blogg",
        "how-to-improve-credit-score": "hur-forbattrar-jag-min-kreditvardighet",
    },
    "en": {
        "lan": "loans",
        "spara-pengar": "savings",
        "basta-sparrantan": "best-interest-rate",
        "kreditkort": "credit-cards",
        "utan-arsavgift": "no-annual-fee",
        "foretagslan": "business-loans",
        "utan-sakerhet": "unsecured",
        "blogg": "blog",
        "hur-forbattrar-jag-min-kreditvardighet": "how-to-improve-credit-score",
    },
}


def translate_url_segment(segment, target_lang):
    """Translate a URL segment to target language."""
    if target_lang == "sv":
        return URL_TRANSLATIONS["sv"].get(segment, segment)
    elif target_lang == "en":
        return URL_TRANSLATIONS["en"].get(segment, segment)
    return segment
