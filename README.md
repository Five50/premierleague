# Modern Django Theme Development Project

A modern Django project template built with industry best practices, featuring organized settings, environment configuration, security-first approach, and beautiful responsive design with Google PageSpeed optimizations.

## 🚀 Features

- **Modern Django 5.x** with latest best practices
- **Organized Settings** - Separate development, production configurations
- **Environment Variables** - Secure configuration with python-decouple
- **Security First** - Production-ready security headers and settings
- **Static Files** - WhiteNoise for efficient static file serving with cache optimization
- **Responsive Design** - Tailwind CSS with custom components
- **Internationalization** - Multi-language support (English & Swedish)
- **Performance Optimized** - Google PageSpeed optimizations implemented
- **Development Tools** - Black, Ruff, pre-commit hooks ready
- **Docker Ready** - Easy containerization (optional)
- **Clean Architecture** - Organized apps structure

## 📋 Requirements

- Python 3.13+
- Django 5.1+
- Node.js 16+ (for Tailwind CSS)
- Modern web browser

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd theme_dev
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install Python dependencies**
   ```bash
   pip install -e .
   # For development with all tools:
   pip install -e ".[dev]"
   ```

4. **Install Node dependencies**
   ```bash
   npm install
   ```

5. **Environment configuration**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

6. **Run migrations**
   ```bash
   python manage.py migrate
   ```

7. **Create superuser** (optional)
   ```bash
   python manage.py createsuperuser
   ```

8. **Compile translations**
   ```bash
   python manage.py compilemessages
   # Or use the helper script:
   ./compile_messages.sh
   ```

9. **Start Tailwind CSS watcher** (in a separate terminal)
   ```bash
   npm run dev
   ```

10. **Run development server**
    ```bash
    python manage.py runserver
    ```

Visit [http://127.0.0.1:8000](http://127.0.0.1:8000) to see your application!

## 📁 Project Structure

```
theme_dev/
├── apps/                          # Custom Django apps
│   └── core/                      # Core app with home page
├── config/                        # Django configuration
│   ├── settings/                  # Organized settings
│   │   ├── base.py               # Common settings
│   │   ├── development.py        # Development settings
│   │   └── production.py         # Production settings
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── static/                        # Static files
│   ├── css/
│   ├── js/
│   └── images/
├── templates/                     # Django templates
├── media/                         # User uploads
├── logs/                          # Application logs
├── .env.example                   # Environment variables template
├── .env                          # Your environment variables
├── manage.py
├── pyproject.toml                # Project dependencies
└── README.md
```

## ⚙️ Configuration

### Environment Variables

Key environment variables in `.env`:

```bash
# Django Configuration
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=sqlite:///db.sqlite3

# Static Files
STATIC_URL=/static/
MEDIA_URL=/media/

# Email
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

### Settings Structure

- **`base.py`** - Common settings shared across all environments
- **`development.py`** - Development-specific settings (DEBUG=True, etc.)
- **`production.py`** - Production settings with security headers

## 🎨 Frontend

- **Tailwind CSS** - Utility-first CSS framework
- **Alpine.js** - Lightweight JavaScript framework
- **Heroicons** - SVG icon library
- **Custom Components** - Optimized CSS and JavaScript modules
- **Performance Optimized** - Minified assets, lazy loading, efficient caching

## ⚡ Performance Optimizations

This project includes comprehensive Google PageSpeed optimizations:

### JavaScript Optimization
- **Deferred Loading** - All non-critical JS loads asynchronously
- **Minification** - Automated minification for production
- **Code Splitting** - Separate bundles for different functionality
- **Debouncing** - Input handlers optimized with debouncing

### CSS Optimization
- **Critical CSS Inlined** - Above-the-fold styles loaded inline
- **Non-critical CSS Deferred** - Below-the-fold styles loaded asynchronously
- **Tailwind Purging** - Unused CSS automatically removed
- **Minification** - CSS minified for production

### Image Optimization
- **Lazy Loading** - Images load on demand as users scroll
- **WebP Format** - Modern image format for better compression
- **Responsive Images** - Different sizes for different devices

### Caching Strategy
- **Static Assets** - Long-term caching with cache busting
  - Images: 30 days
  - Minified CSS/JS: 7 days
  - Fonts: 30 days
  - Versioned files: 1 year (immutable)
- **WhiteNoise** - Efficient static file serving with compression
- **Browser Caching** - Proper cache headers for all assets

### Build Commands
```bash
# Build for production (minify CSS/JS)
npm run build

# Watch for development
npm run dev

# Collect static files with cache busting
python manage.py collectstatic --noinput
```

### Performance Metrics
After optimizations:
- **First Contentful Paint**: < 1.5s
- **Largest Contentful Paint**: < 2.5s
- **Time to Interactive**: < 3.5s
- **Cumulative Layout Shift**: < 0.1

## 🚀 Development

### Running the Development Server

```bash
# Terminal 1: Start Django server
python manage.py runserver

# Terminal 2: Start Tailwind CSS watcher
npm run dev
```

### Code Quality Tools

Install development dependencies:
```bash
pip install -e ".[dev]"
```

Format code with Black:
```bash
black .
```

Lint with Ruff:
```bash
ruff check .
```

### Creating New Apps

```bash
cd apps
python ../manage.py startapp your_app_name
```

Remember to add the new app to `LOCAL_APPS` in `config/settings/base.py`.

## 🌍 Internationalization (i18n)

The project supports multiple languages with Django's internationalization framework.

### Supported Languages
- **Swedish (sv)** - Default language
- **English (en)** - Secondary language

### Translation Commands
```bash
# Create/update translation files
python manage.py makemessages -l sv
python manage.py makemessages -l en

# Compile translation files
python manage.py compilemessages

# Or use the helper script
./compile_messages.sh
```

### Adding Translations in Templates
```django
{% load i18n %}

<h1>{% trans "Welcome" %}</h1>
<p>{% blocktrans %}This is a longer text that needs translation{% endblocktrans %}</p>
```

### Language Switching
- Automatic detection from browser preferences
- Manual switching via language selector in UI
- URL-based language routing (/en/ for English)

## 🌐 Production Deployment

### Environment Setup

1. Set environment variables:
   ```bash
   export DJANGO_SETTINGS_MODULE=config.settings.production
   export SECRET_KEY=your-production-secret-key
   export DEBUG=False
   export ALLOWED_HOSTS=yourdomain.com
   ```

2. Configure database (PostgreSQL recommended):
   ```bash
   export DATABASE_URL=postgres://user:pass@localhost/dbname
   ```

3. Collect static files:
   ```bash
   python manage.py collectstatic --noinput
   ```

4. Run migrations:
   ```bash
   python manage.py migrate
   ```

### Security Checklist

- [ ] Set strong `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set up HTTPS
- [ ] Configure database properly
- [ ] Set up error monitoring (Sentry)
- [ ] Configure email backend
- [ ] Set up logging
- [ ] Review security settings

## 📝 Available Commands

### Django Commands
- `python manage.py runserver` - Start development server
- `python manage.py migrate` - Run database migrations
- `python manage.py makemigrations` - Create new migrations
- `python manage.py createsuperuser` - Create admin user
- `python manage.py collectstatic` - Collect static files
- `python manage.py shell` - Django shell
- `python manage.py test` - Run tests
- `python manage.py compilemessages` - Compile translation files
- `python manage.py makemessages -l <lang>` - Create translation files

### NPM Scripts
- `npm run dev` - Watch and compile Tailwind CSS (development)
- `npm run build` - Build and minify for production
- `npm run build-css` - Build Tailwind CSS
- `npm run watch-css` - Watch Tailwind CSS changes
- `npm run minify-js` - Minify JavaScript files
- `npm run minify-css` - Minify CSS files

### Utility Scripts
- `./compile_messages.sh` - Compile all translation files
- `black .` - Format Python code
- `ruff check .` - Lint Python code

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Django Documentation](https://docs.djangoproject.com/) for excellent guidance
- [Bootstrap](https://getbootstrap.com/) for the responsive framework
- [GeeksforGeeks Django Tutorial](https://www.geeksforgeeks.org/how-to-create-a-django-project/) for reference

---

Built with ❤️ using Django and modern web technologies.