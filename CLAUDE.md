# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a modern Django 5.x Premier League website built for Swedish audiences with organized settings, environment-based configuration, and best practices for theme development. The project uses Python 3.13+ and follows a clean architecture pattern with internationalization (i18n) support and Tailwind CSS for styling. The site focuses on Premier League content, news, fixtures, and team information with Swedish as the primary language and English as a secondary language.

## Commands

### Development Setup
```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e .

# Install dev dependencies
pip install -e ".[dev]"

# Install Node dependencies for Tailwind CSS
npm install

# Copy environment variables
cp .env.example .env

# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

### Tailwind CSS & Asset Pipeline
```bash
# Watch and compile Tailwind CSS (development)
npm run dev

# Build all assets (CSS, JS minification, compression)
npm run build

# Build only minified CSS
npm run build-css-min

# Build for production (minified CSS + compression)
npm run build:production

# Individual build tasks
npm run build-css          # Build CSS without minification
npm run minify-js          # Minify JavaScript files
npm run minify-css         # Minify business-loans.css
npm run compress-static    # Compress static files with Python script
```

### Internationalization
```bash
# Create/update translation files
python manage.py makemessages -l sv
python manage.py makemessages -l en

# Compile translation files
python manage.py compilemessages

# Or use the helper script
./compile_messages.sh
```

### Code Quality
```bash
# Format code with Black
black .

# Lint with Ruff
ruff check .
```

### Django Commands
```bash
# Create new app (from project root)
cd apps
python ../manage.py startapp your_app_name

# Make migrations
python manage.py makemigrations

# Run tests
python manage.py test

# Test error pages
python test_error_pages.py
```

## Architecture

### Project Structure
- **apps/** - All Django apps are located here to keep them organized
  - `core/` - Main application with views, models, and utilities
- **config/** - Django configuration with separate settings for dev/prod
  - `settings/` - Environment-specific settings (base, development, production)
  - `urls.py` - Main URL configuration
  - `wsgi.py` & `asgi.py` - Application server interfaces
- **templates/** - Global templates using Atomic Design methodology
  - `atoms/` - Basic UI elements (buttons, inputs, etc.)
  - `molecules/` - Combinations of atoms (forms, cards, etc.)
  - `organisms/` - Complex UI components (headers, sections, etc.)
  - `pages/` - Full page templates
  - `templates/` - Base templates
  - Error pages (400.html, 403.html, 404.html, 500.html)
- **static/** - Static files (CSS, JS, images)
  - `css/input.css` - Tailwind CSS input file with custom styles
  - `css/output.css` - Compiled Tailwind CSS output
  - `css/business-loans.css` - Business loan specific styles
  - `js/business-loans.js` - Business loan JavaScript functionality
  - `images/` - Image assets including logos and icons
- **staticfiles/** - Collected static files for production
- **media/** - User-uploaded files
- **locale/** - Translation files for internationalization (en, sv)
- **logs/** - Application logs
- **docs/** - Project documentation

### Settings Organization
- **config/settings/base.py** - Common settings shared across all environments
- **config/settings/development.py** - Development-specific settings (DEBUG=True)
- **config/settings/production.py** - Production settings with security headers
- Default settings module is `config.settings.development` (see manage.py:9)

### Key Configuration
- Environment variables are managed with python-decouple
- Settings are accessed via `config()` function with defaults
- Apps directory is added to Python path for clean imports (base.py:19)
- WhiteNoise is configured for static file serving
- Django-compressor for CSS/JS compression in production

### Internationalization (i18n)
- Multi-language support (Swedish primary, English secondary)
- Swedish is the default language for this Premier League site
- Language preference stored in session
- Language switcher available in the UI
- Automatic language detection from browser preferences
- Translation files in `locale/` directory (sv, en)
- Custom middleware for language handling

### Frontend Stack
- **Tailwind CSS** - Utility-first CSS framework (using standalone CLI binary)
- **Alpine.js** - Lightweight JavaScript framework for interactivity
- **Heroicons** - SVG icon library
- **PostCSS** - CSS processing with cssnano for minification
- **Terser** - JavaScript minification
- Responsive design with mobile-first approach
- Dark mode support with CSS variables
- Atomic Design pattern for template organization

### Template Organization (Atomic Design)
The project follows Atomic Design methodology for template organization:

- **templates/atoms/** - Basic building blocks
  - Buttons, inputs, labels, icons, etc.
- **templates/molecules/** - Groups of atoms
  - Form groups, cards, navigation items, etc.
- **templates/organisms/** - Complex components
  - Headers, footers, forms, sections, tables, etc.
  - Business-specific components (loan calculators, interest rate displays)
- **templates/pages/** - Complete page layouts
  - Home, about, services, contact pages, etc.
- **templates/templates/** - Base layouts and includes
  - Base template structure
- **Error Pages** - Custom error templates (400, 403, 404, 500)

### App Development
- New apps should be created in the apps/ directory
- Add new apps to LOCAL_APPS in config/settings/base.py
- Follow existing patterns in apps/core for structure
- Use Django's translation utilities for all user-facing text
- Include app-specific template tags in `templatetags/` directory

### Database
- Default: SQLite3 for development
- Production: Can use PostgreSQL via DATABASE_URL environment variable
- Migrations are stored in each app's migrations/ directory

### Security & Middleware
- Custom security middleware for production
- CSRF protection enabled
- XSS protection headers
- Language preference middleware
- WhiteNoise for secure static file serving

## Additional Files

### Helper Scripts
- **tailwindcss** - Standalone Tailwind CSS binary for compilation
- **compile_messages.sh** - Helper script for compiling translations
- **fix_translations.py** - Script to fix translation issues
- **test_error_pages.py** - Script to test custom error pages

### Configuration Files
- **.env.example** - Example environment variables file
- **pyproject.toml** - Python project configuration and dependencies
- **package.json** - Node.js dependencies and scripts
- **postcss.config.js** - PostCSS configuration for CSS processing
- **.python-version** - Python version specification
- **.gitignore** - Git ignore patterns

## Development Workflow

1. **Starting a new feature:**
   - Create a new branch from main
   - Run `npm run dev` to start Tailwind CSS watcher
   - Run `python manage.py runserver` to start Django server

2. **Adding new templates:**
   - Follow Atomic Design principles
   - Start with atoms, build up to molecules, then organisms
   - Use existing components where possible

3. **Working with translations:**
   - Add translatable strings using Django's i18n tags
   - Run `python manage.py makemessages` to extract strings
   - Update translation files in locale/
   - Run `./compile_messages.sh` to compile

4. **Building for production:**
   - Run `npm run build:production` to build and minify assets
   - Run `python manage.py collectstatic` to gather static files
   - Ensure all tests pass with `python manage.py test`

## Common Patterns

### Premier League Components
The project includes templates for Premier League football content:
- Team pages with club information and statistics
- Match fixtures and results displays
- Player statistics and profiles
- League tables and standings
- News articles and match reports
- Live match updates and scoring systems

### Responsive Design
- Mobile-first approach using Tailwind CSS
- Breakpoints: sm (640px), md (768px), lg (1024px), xl (1280px), 2xl (1536px)
- All components should be tested on mobile and desktop

### CSS Organization
- Use Tailwind utility classes primarily
- Custom CSS in `static/css/input.css` with Premier League theming
- Premier League team colors and branding throughout
- Responsive design for mobile and desktop football fans
- Avoid inline styles; use Tailwind classes instead