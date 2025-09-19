from django import template
from django.urls import resolve, reverse
from django.urls.exceptions import Resolver404
from django.utils.translation import activate, get_language

register = template.Library()


@register.simple_tag(takes_context=True)
def translate_url(context, lang_code):
    """
    Get the current page's URL in the specified language.
    """
    request = context.get("request")
    if not request:
        return ""

    # Get the current path
    path = request.path

    # Store current language
    current_lang = get_language()

    try:
        # Clean path - remove any language prefix
        clean_path = path
        if path.startswith("/en/"):
            clean_path = path[3:]  # Remove '/en' prefix
        elif path == "/en":
            clean_path = "/"

        # Special handling for homepage
        if clean_path == "/" or clean_path == "":
            activate(lang_code)
            url = reverse("home")
            activate(current_lang)
            return url

        # Try to resolve the URL
        # For English URLs, we need to resolve with English active
        if path.startswith("/en/"):
            activate("en")
            # Try to resolve the clean path
            try:
                match = resolve(clean_path)
            except Resolver404:
                # If that fails, try with the full path
                match = resolve(path)
        else:
            activate("sv")
            match = resolve(clean_path)

        # Now activate the target language and generate URL
        activate(lang_code)
        url = reverse(match.url_name, kwargs=match.kwargs)

    except (Resolver404, AttributeError, Exception):
        # If we can't resolve, just switch the language prefix
        if lang_code == "en":
            if path.startswith("/en/"):
                url = path  # Already has English prefix
            else:
                url = f"/en{path}" if path != "/" else "/en/"
        else:
            if path.startswith("/en/"):
                url = path[3:] if len(path) > 4 else "/"
            else:
                url = path  # Already Swedish (no prefix)

    finally:
        # Restore original language
        activate(current_lang)

    return url


@register.simple_tag(takes_context=True)
def get_alternate_languages(context):
    """
    Get all available language versions of the current page.
    Returns a list of tuples (lang_code, url, lang_name)
    """
    request = context.get("request")
    if not request:
        return []

    from django.conf import settings

    alternates = []
    current_lang = get_language()

    for lang_code, lang_name in settings.LANGUAGES:
        url = translate_url(context, lang_code)
        alternates.append(
            {
                "code": lang_code,
                "url": request.build_absolute_uri(url),
                "name": lang_name,
                "is_current": lang_code == current_lang,
            }
        )

    return alternates


@register.filter
def dict_item(dictionary, key):
    """
    Get item from dictionary by key
    """
    try:
        return dictionary.get(key)
    except (AttributeError, TypeError):
        return None
