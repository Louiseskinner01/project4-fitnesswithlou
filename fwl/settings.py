import os
import dj_database_url
from pathlib import Path

# Import environment variables from env.py if it exists (local development only)
# env.py is in .gitignore so secret keys are never pushed to GitHub
if os.path.isfile('env.py'):
    import env
    
# Load environment variables from .env file if it exists
from dotenv import load_dotenv
load_dotenv()

# Stripe API keys - loaded from environment variables for security
STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')
STRIPE_PUBLIC_KEY = os.environ.get('STRIPE_PUBLIC_KEY')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR points to the root of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# SECRET_KEY is used by Django for cryptographic signing
# In production this comes from Heroku Config Vars
# The fallback value is only used locally
SECRET_KEY = os.environ.get('SECRET_KEY', 'jango-insecure--wwc4!o8$lapuxv!@l*(isu_s&=jd#y7zanwc%ag6fr0*8qkjh')

# DEBUG mode shows detailed error pages - must be False in production
# Reads from environment variable, defaults to False if not set
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
#DEBUG = 'True'

# List of hostnames that Django will serve requests for
# Prevents HTTP Host header attacks
ALLOWED_HOSTS = [
    'only-parsley-vocalize.ngrok-free.dev',  # ngrok URL for local webhook testing
    '127.0.0.1',                              # local development
    'localhost',                              # local development
    'project4-fwl-ce947c9798e9.herokuapp.com', # production Heroku URL
]

# All Django apps that are installed and active in this project
INSTALLED_APPS = [
    # Django built-in apps
    'django.contrib.admin',        # Admin interface
    'django.contrib.auth',         # Authentication system
    'django.contrib.contenttypes', # Content type framework
    'django.contrib.sessions',     # Session framework
    'django.contrib.messages',     # Messaging framework
    'django.contrib.staticfiles',  # Static file management
    'cloudinary_storage',          # Cloudinary media storage (must come after staticfiles)
    'cloudinary',                  # Cloudinary integration
    'django.forms',                # Django forms
    
    # Project apps
    'users',          # User profiles
    'products',       # Product catalogue
    'bookings',       # Class bookings
    'cart',           # Shopping cart
    'subscriptions',  # Membership subscriptions
    'checkout',       # Checkout and payments
    'nutrition',      # Nutritional advice
    'main',           # Main pages (landing, about, etc)
    'accounts',       # Custom account forms
    
    # Django sites framework (required by allauth)
    'django.contrib.sites',
    
    # Allauth - handles authentication, registration and email verification
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    
    # Crispy forms - renders Django forms with Bootstrap styling
    'crispy_forms',
    'crispy_bootstrap5',
]

# Middleware is processed in order for every request and response
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',           # Security headers
    'whitenoise.middleware.WhiteNoiseMiddleware',              # Serves static files in production
    'django.contrib.sessions.middleware.SessionMiddleware',    # Session handling
    'allauth.account.middleware.AccountMiddleware',            # Allauth account middleware
    'django.middleware.common.CommonMiddleware',               # Common HTTP operations
    'django.middleware.csrf.CsrfViewMiddleware',               # CSRF protection
    'django.contrib.auth.middleware.AuthenticationMiddleware', # Authentication
    'django.contrib.messages.middleware.MessageMiddleware',    # Flash messages
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Clickjacking protection
]

# Root URL configuration file
ROOT_URLCONF = 'fwl.urls'

# Tell crispy forms to use Bootstrap 5 styling
CRISPY_TEMPLATE_PACK = 'bootstrap5'

# Template engine configuration
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),  # Project level templates folder
        ],
        'APP_DIRS': True,  # Also look for templates in each app's templates folder
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',    # Adds debug variable to templates
                'django.template.context_processors.request',  # Adds request object to templates
                'django.contrib.auth.context_processors.auth', # Adds user and perms to templates
                'django.contrib.messages.context_processors.messages', # Adds messages to templates
                'django.template.context_processors.media',    # Adds MEDIA_URL to templates
                'cart.contexts.cart_contents',                 # Adds cart data to all templates
            ],
            'builtins': [
                # Load crispy forms tags globally so they don't need to be loaded in every template
                'crispy_forms.templatetags.crispy_forms_tags',
                'crispy_forms.templatetags.crispy_forms_field',
            ]
        },
    },
]

# Store flash messages in the session rather than cookies
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

# Authentication backends - defines how users can log in
AUTHENTICATION_BACKENDS = [
    # Standard Django auth - allows login via Django admin
    'django.contrib.auth.backends.ModelBackend',
    # Allauth backend - allows login via email
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Required by Django sites framework and allauth
SITE_ID = 1

# Default from email address for system emails
DEFAULT_FROM_EMAIL = 'fitnesswithlouise@gmail.com'

# Email configuration - uses console backend locally, Gmail SMTP in production
if 'DEVELOPMENT' in os.environ:
    # Print emails to terminal instead of sending them during development
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    # Send real emails via Gmail SMTP in production
    EMAIL_USE_TLS = True                                          # Use TLS encryption
    EMAIL_PORT = 587                                              # Gmail SMTP port
    EMAIL_HOST = 'smtp.gmail.com'                                 # Gmail SMTP server
    EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')          # Gmail address
    EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')  # Gmail app password
    DEFAULT_FROM_EMAIL = os.environ.get('EMAIL_HOST_USER')       # Use Gmail as from address

# Allauth configuration
ACCOUNT_LOGIN_METHODS = {"username", "email"}  # Allow login with username or email
ACCOUNT_SIGNUP_FIELDS = ["email*", "email2*", "username*", "password1*", "password2*"]  # Required signup fields
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'  # Users must verify email before logging in
ACCOUNT_USERNAME_MIN_LENGTH = 4           # Minimum username length
LOGIN_URL = '/accounts/login/'            # URL to redirect to when login is required
LOGIN_REDIRECT_URL = '/'                  # Redirect here after login
LOGOUT_REDIRECT_URL = '/'                 # Redirect here after logout

# Use custom login form
ACCOUNT_FORMS = {'login': 'accounts.forms.CustomLoginForm',}

# WSGI application entry point
WSGI_APPLICATION = 'fwl.wsgi.application'

# Database configuration
# Uses Postgres on Heroku (DATABASE_URL set in Config Vars)
# Falls back to SQLite for local development
if 'DATABASE_URL' in os.environ:
    DATABASES = {
        'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Password validation rules
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalisation settings
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True   # Enable Django's translation system
USE_TZ = True     # Use timezone-aware datetimes

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'                                          # URL prefix for static files
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)          # Where to find static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')             # Where collectstatic copies files to

# Storage backends
# default: Cloudinary for media files (product images, CVs etc) - persists permanently
# staticfiles: WhiteNoise for static files (CSS, JS) - served efficiently in production
STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

# Media files (user uploaded content)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # Local media storage (used in development)

# Default primary key type for models
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Stripe payment configuration
FREE_DELIVERY_ABOVE = 35    # Free delivery threshold in pounds
DELIVERY_PERCENTAGE = 10    # Delivery charge percentage below threshold
STRIPE_CURRENCY = 'gbp'     # Currency for Stripe payments
STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PUBLIC_KEY', '')   # Stripe publishable key (frontend)
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY', '')   # Stripe secret key (backend)
STRIPE_WH_SECRET = os.environ.get('STRIPE_WH_SECRET', '') # Stripe webhook signing secret

# Stripe subscription price IDs (from Stripe dashboard)
STRIPE_PRICE_BASIC = 'price_1Tdxlq2dKqODld9JLf49TBdQ'    # Basic plan monthly price
STRIPE_PRICE_PREMIUM = 'price_1TdyQm2dKqODld9JXREF6k87'  # Premium plan monthly price
STRIPE_PRICE_VIP = 'price_1TdyPZ2dKqODld9JImPfOYsJ'      # VIP plan monthly price

# Use Django's template-based form rendering
FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'

# Trusted origins for CSRF protection
# These domains are allowed to make POST requests to the site
CSRF_TRUSTED_ORIGINS = [
    'https://project4-fwl-ce947c9798e9.herokuapp.com',  # Production Heroku URL
    'https://only-parsley-vocalize.ngrok-free.dev',      # ngrok URL for local testing
    'http://127.0.0.1',                                  # Local development
    'http://localhost',                                  # Local development
]

