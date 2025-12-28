"""
Django settings for cerberus_ref project.
"""
import os
import sys
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Add the cerberus middleware to Python path (relative to this file)
# This file is in cerberus-ref/cerberus_ref/, middleware is in cerberus/src/
CERBERUS_MIDDLEWARE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'cerberus', 'src'))
if CERBERUS_MIDDLEWARE_PATH not in sys.path:
    sys.path.insert(0, CERBERUS_MIDDLEWARE_PATH)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-dev-key-change-in-production'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Cerberus middleware - must be after auth middleware to access request.user
    'cerberus_ref.cerberus_middleware.CerberusMiddleware',
]

ROOT_URLCONF = 'cerberus_ref.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'cerberus_ref.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Logging Configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'cerberus_django': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

# Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
}

# CORS Configuration (for frontend testing)
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:8080",
]

CORS_ALLOW_METHODS = [
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
    'OPTIONS',
]

# Cerberus Configuration
CERBERUS_CONFIG = {
    # API key for authenticating with the Cerberus backend
    # Get this from the cerberus-int backend (from api_keys table)
    # Sent via X-API-Key header when fetching secret key
    'token': os.getenv('CERBERUS_API_KEY', 'sk-test-key-change-me'),

    # Client ID - identifies this application in the backend
    # Should match a client_id in the api_keys table
    'client_id': os.getenv('CERBERUS_CLIENT_ID', 'test-client'),

    # WebSocket URL for sending events to backend
    # This should point to the event_ingest WebSocket endpoint
    'ws_url': os.getenv('CERBERUS_WS_URL', 'ws://localhost:8001/ws/events'),

    # Backend URL for auto-fetching the HMAC secret key (HTTP endpoint)
    # This should point to the event_ingest service
    'backend_url': os.getenv('CERBERUS_BACKEND_URL', 'http://localhost:8001'),

    # Optional: Manually configure HMAC secret key if backend_url is not available
    # 'secret_key': os.getenv('CERBERUS_SECRET_KEY', 'your-hmac-secret-key'),
}
