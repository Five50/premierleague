# Internationalization (i18n) Implementation

This document describes the multi-language support implementation for the theme_dev project.

## Overview

The application supports two languages:
- **Swedish (sv)** - Default language, no URL prefix
- **English (en)** - Secondary language, uses `/en/` URL prefix

## Configuration

### Django Settings (config/settings/base.py)
```python
LANGUAGE_CODE = 'sv'  # Swedish as default
LANGUAGES = [
    ('sv', _('Svenska')),
    ('en', _('English')),
]
LOCALE_PATHS = [BASE_DIR / 'locale']
```

### Middleware
1. `django.middleware.locale.LocaleMiddleware` - Django's built-in language detection
2. `config.middleware.LanguageFromURLMiddleware` - Custom middleware for URL-based language detection

## URL Structure

### Swedish URLs (default, no prefix)
- `/` - Home
- `/spara-pengar/basta-sparrantan/` - Best savings rate
- `/lan/` - Loans
- `/kreditkort/utan-arsavgift/` - Credit cards without annual fee
- `/foretagslan/utan-sakerhet/` - Unsecured business loans
- `/blogg/` - Blog

### English URLs (with /en/ prefix)
- `/en/` - Home
- `/en/savings/best-interest-rate/` - Best savings rate
- `/en/loans/` - Loans
- `/en/credit-cards/no-annual-fee/` - Credit cards without annual fee
- `/en/business-loans/unsecured/` - Unsecured business loans
- `/en/blog/` - Blog

## Translation Files

Translation files are located in:
- `/locale/sv/LC_MESSAGES/django.po` - Swedish translations
- `/locale/en/LC_MESSAGES/django.po` - English translations

To update translations:
1. Edit the `.po` files
2. Run: `python manage.py compilemessages`

## Language Switcher

A language switcher component is available in the header:
- Location: `templates/molecules/language-switcher.html`
- Uses Django's built-in language switching view at `/i18n/setlang/`

## Content Translation

### Static Content
- Menu items and UI text use Django's translation system
- Translation strings are defined in `.po` files

### Dynamic Content
- Page content is managed through `apps/core/translations.py`
- Views access translations based on current language
- Content structure supports both languages

## Usage in Templates

```django
{% load i18n %}
{% trans "Text to translate" %}
{% get_current_language as LANGUAGE_CODE %}
```

## Usage in Views

```python
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language

current_language = get_language()
```

## Development Workflow

1. Add new translatable strings using `_()` or `{% trans %}`
2. Run `python manage.py makemessages -l sv -l en` to update `.po` files
3. Translate the strings in the `.po` files
4. Run `python manage.py compilemessages` to compile translations
5. Test both languages by switching in the UI or accessing URLs directly